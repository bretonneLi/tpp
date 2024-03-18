<?php
/**
 * Plugin Name:       Tingyimiao-Panda-Page
 * Description:       Panda page plugin with reactjs.
 * Requires at least: 5.8
 * Requires PHP:      7.0
 * Version:           0.1.0
 * Author:            Patrick Zeng
 * License:           GPL-2.0-or-later
 * License URI:       https://www.tingyimiao.com
 * Text Domain:       pandapage
 */

 add_action( 'admin_menu', 'jobplace_init_menu' );

/**
 * Init Admin Menu.
 *
 * @return void
 */
function jobplace_init_menu() {
    // menu icon base64
    $menuicon = 'PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxZW0iIGhlaWdodD0iMWVtIiB2aWV3Qm94PSIwIDAgMjQgMjQiPjxwYXRoIGZpbGw9ImN1cnJlbnRDb2xvciIgZD0iTTkgN3YyaDJ2OGgyVjloMlY3em0zLTVhMTAgMTAgMCAwIDEgMTAgMTBhMTAgMTAgMCAwIDEtMTAgMTBBMTAgMTAgMCAwIDEgMiAxMkExMCAxMCAwIDAgMSAxMiAyIi8+PC9zdmc+';
    add_menu_page( __( 'Panda', 'pandapage'), __( 'Panda', 'pandapage'), 'manage_options', 'pandapage', 'jobplace_admin_page', 'data:image/svg+xml;base64,'.$menuicon, '2.1' );
}

/**
 * Init Admin Page.
 *
 * @return void
 */
function jobplace_admin_page() {
    require_once plugin_dir_path( __FILE__ ) . 'templates/app.php';
}

add_action( 'admin_enqueue_scripts', 'jobplace_admin_enqueue_scripts' );

/**
 * Enqueue scripts and styles.
 *
 * @return void
 */
function jobplace_admin_enqueue_scripts() {
    wp_enqueue_style( 'jobplace-style', plugin_dir_url( __FILE__ ) . 'build/index.css' );
    wp_enqueue_script( 'jobplace-script', plugin_dir_url( __FILE__ ) . 'build/index.js', array( 'wp-element' ), '1.0.0', true );
}

// add api route hook
add_action( 'rest_api_init', 'register_api_route' );
/**
 * register embedding web restful api from wordpress
 */
function register_api_route(){
    // add embedding file record to wp table
    register_rest_route('embedding/v1', '/save', array(
        'methods' => 'POST',
        'callback' => 'add_embedding_record',
    ));

    // update embedding file processing status
    register_rest_route('embedding/v1','/update', array(
        'methods' => 'POST',
        'callback' => 'update_embedding_records',
    ));

    // get file uploaded list
    register_rest_route('embedding/v1', '/list', array(
        'methods' => 'GET',
        'callback' => 'get_embedding_records',
    ));

    // set llm setting record to wp table
    register_rest_route('llm/v1', '/set', array(
        'methods' => 'POST',
        'callback' => 'setLLM',
    ));

     // get llm support list
     register_rest_route('llm/v1', '/target', array(
        'methods' => 'GET',
        'callback' => 'getCurrLLM',
    ));
}

// 加载当前登录用户信息
add_action('init','do_stuff');
function do_stuff(){
  $current_user = wp_get_current_user();
//   print_r($current_user);  加了这句才能在后面代码里面获取用户信息
  return $current_user;
}

/**
 * add embedding record to table in word press database
 */
function add_embedding_record(WP_REST_Request $request) {
    // $current_user = do_stuff();
    $userInfo = do_stuff();
    // login username
    // $username =  $current_user->data->user_login;
    // for test only
    $username = 'admin';

    global $wpdb;
    $table_name = $wpdb->prefix . 'embedding_records';
    $parameters = json_decode($request->get_body());
    $fileName = $parameters->fileName;
    $fileStatus = 'In-progress';
    $fileSize = $parameters->fileSize;

    if($fileName) {
      $insert = $wpdb->insert($table_name, array(
          "file_name" => $fileName ,
          "file_size" => $fileSize,
          "owner" => $username,
          "file_status" => $fileStatus,
          ));
      if($insert) {
        // new id generated after inserted to table
        return $wpdb->insert_id;
      } else {
        return 0;
      }
    }
    return -1;
}

/**
 * update embedding record info
 */
function update_embedding_records(WP_REST_Request $request){
    global $wpdb;
    $table_name = $wpdb->prefix . 'embedding_records';
    $parameters = json_decode($request->get_body());
    $embId = $parameters->embId;
    $fileStatus = $parameters->fileStatus;
    $vectorIds = $parameters->vectorIds;
    $vectorPath = $parameters->vectorPath;

    if($embId) {
        // query first 
        $results = $wpdb->get_results( 
            $wpdb->prepare( "SELECT 1 FROM {$wpdb->prefix}embedding_records WHERE emb_id=%d", $embId ) 
        );
        if($results){
            $update_array = array();
            $update_array['file_status'] = $fileStatus;
            if($vectorIds){
                $update_array['vector_ids'] = $vectorIds;
            }

            if($vectorPath){
                $update_array['vector_path'] = $vectorPath;
            }
            $wpdb->update(
                $table_name, 
                $update_array,
                array('emb_id' => $embId)
            );
            return 'ok'; 
        }
        return 'error'; 
    }

    return 'paramenter error';
}

/**
 * query uploaded embedding records by owner specified
 */
function get_embedding_records(WP_REST_Request $request){
    global $wpdb;
    $table_name = $wpdb->prefix . 'embedding_records';
    $parameters = $request->get_params();
    $owner = $parameters['owner'];
  
    if($owner) {
        $results = $wpdb->get_results(
            "SELECT * FROM $table_name where `owner` = '$owner' and `file_status` <>'deleted' order by file_datetime desc; "
        );

        return $results;
    }
    // return empty array
    return [];
}

/**
 * set current LLM name to data table
 */
function setLLM(WP_REST_Request $request){
     $userInfo = do_stuff();
     // login username
     // $username =  $current_user->data->user_login;
     // for test only
     $username = 'admin';
 
     global $wpdb;
     $table_name = $wpdb->prefix . 'llm_setting';
     $parameters = json_decode($request->get_body());
     $llmName = $parameters->llmName;
 
     if($llmName) {
       $insert = $wpdb->insert($table_name, array(
           "llm_name" => $llmName ,
           "created_by" => $username
           ));
       if($insert) {
         // new id generated after inserted to table
         return $wpdb->insert_id;
       } else {
         return 0;
       }
     }
     return -1;
}

/**
 * get current LLM set already
 */
function getCurrLLM(WP_REST_Request $request){
    global $wpdb;
    $table_name = $wpdb->prefix . 'llm_setting';
  
    $results = $wpdb->get_results(
        "select llm_name from $table_name order by id desc limit 1;"
    );

    if(empty($results)>0){
        return $results[0];
    }
    // return empty
    return "";
}
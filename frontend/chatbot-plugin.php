<?php
/**
 * Plugin Name:       TPP-Chatbot
 * Description:       TPP chatbot plugin with reactjs.
 * Requires at least: 5.8
 * Requires PHP:      7.0
 * Version:           0.1.0
 * Author:            Patrick Zeng
 * License:           GPL-2.0-or-later
 * License URI:       https://www.tingyimiao.com
 * Text Domain:       chatbot
 */

wp_enqueue_style( "tpp-chatbot-style", plugin_dir_url( __FILE__ ) . "build/index.css" );

wp_enqueue_script( "tpp-chatbot-script", plugin_dir_url( __FILE__ ) . "build/index.js" , array( 'wp-element' ), '1.0.0', true);

add_action("wp_footer", function(){
    echo '<div id="tppchatbot"></div>';
});
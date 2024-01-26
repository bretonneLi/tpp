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
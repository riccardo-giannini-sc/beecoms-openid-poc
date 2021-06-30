<?

require_once "config.php";

//http://127.0.0.1:8002/o/authorize/?response_type=code&client_id=3acdP8a40lynGYntwY6[…]fPtuC7aNy&redirect_uri=http://127.0.0.1:8002/noexist/callback

function get_serverapp_client_id(string $url): string
{
    $ch = curl_init($url);
    return curl_exec($ch);
}

$data = http_build_query([
    "response_type" => "code",
    "client_id" => get_serverapp_client_id($serverapp_client_id_endpoint),
    "redirect_uri" => $redirect_uri,
]);

$prm_oauth_login_url = "{$prm_base_url}/o/authorize/?{$data}";

ob_start();

?>

<form action="<?= $prm_oauth_login_url ?? '' ?>">
<button>Login in PRM</button>
</form>

<?
$content = ob_get_contents();
ob_end_clean();

require_once "index.php";
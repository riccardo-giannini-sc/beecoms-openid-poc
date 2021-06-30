<?

require_once "config.php";

ob_start();

?>

<h1>Login in App</h1>

<form action="<?=$serverapp_base_url?>/prm_resource" method="GET">
<button>Prendi Risorsa</button>
</form>

<?
$content = ob_get_contents();
ob_end_clean();

require_once "index.php";
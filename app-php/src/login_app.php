<?

require_once "config.php";

if ($_POST['username'] && $_POST['password']) {

    $username = preg_replace('/[^-a-zA-Z0-9_]/', '', $_POST['username']);
    $password = preg_replace('/[^-a-zA-Z0-9_]/', '', $_POST['password']);


    if ($_POST['test-always-fail']) {
        $error = "Spiacente, non sei autenticato";
    } else {
        $ch = curl_init("{$serverapp_base_url}/oauth/login/");
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode(['username' => $username, 'password' => $password]));
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

        // var_dump("httpcode e response and oauth/login", $httpcode, $response);

        if ($httpcode == 200) {
            setcookie("logged_in_app", true);
            header("Location: /login_prm.php");
            exit();
        } else {
            $error = "Spiacente, non sei autenticato";
        }
    }
}
if ($_POST['logout']) {
    $ch = curl_init("{$serverapp_base_url}/oauth/logout/");
    curl_setopt($ch, CURLOPT_POST, true);

    $response = curl_exec($ch);
    $httpcode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

    if ($httpcode == 200) {
        setcookie("logged_in_app", true);
        header("Location: /login_app.php");
        exit();
    } else {
        echo "Spiacente, logout andato male";
    }
}

ob_start();

?>

<h1>Login in App</h1>

<form action="login_app.php" method="POST">
<label for="username">Username:</label>
<input name="username" type="text" placeholder="username">
<br/>
<label for="password">Password:</label>
<input name="password" type="password" placeholder="password">
<br/>
<!-- <label for="test-always-fail">Test: if checked, the login always fails:</label> -->
<!-- <input name="test-always-fail" type="checkbox" value="1"> -->
<!-- <br/> -->
<button>Login in App</button>
<br/>
<span style="color:red"><?=$error ?? ''?></span>
<br/>
</form>

<?
$content = ob_get_contents();
ob_end_clean();

if ($_COOKIE['logged_in_app']) {
    ob_start();

?>

<h1>Logout</h1>

<form action="login_app.php" method="POST">
<input name="logout" type="hidden" value="1">
<button>Logout</button>
<br/>
</form>

<?
$content = ob_get_contents();
ob_end_clean();
}

require_once "index.php";

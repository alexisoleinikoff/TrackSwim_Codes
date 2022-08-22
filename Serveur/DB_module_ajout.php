<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr">

    <head>
        <meta charset="utf8">
        <title>Administrateur</title>
        <link rel="stylesheet" href="style.css">

        <!-- Script pour l'ouverture de la bannière-->
        <script src="jquery.js"></script>
        <script>
            $(function(){
                $("#includedBanner").load("banner.html"); 
            });
        </script>
        <link rel="icon" href="Media\TrackSwim_logo\ts_icon.ico">
    </head>

    <body>
        <!-- Bannière -->
        <div id="includedBanner"></div>
        <center>

        <?php
            include 'path_BD.php';

            try
            {
                $bdd = new PDO($mon_Path_BD, $mon_userName, $monPSW);
                #echo "BD ouverte <BR>";
            }
            catch (Exception $e)
            {
                die('Erreur : ' . $e->getMessage());
            }

            if (!empty($_POST['MODULE_TO_ADD_MODE']) and !empty($_POST['MODULE_TO_ADD_POOL'])) {
                $bdd->query("INSERT INTO module (Mode, ID_piscine) VALUES ('".$_POST['MODULE_TO_ADD_MODE']."', '".$_POST['MODULE_TO_ADD_POOL']."')");
                $newid = $bdd->query("SELECT @@IDENTITY");
                $newid = $newid->fetch();
                if (!empty($newid) and $newid[0] != 0) {
                    echo "<strong>Succès</strong><br>Identifiant propre du nouveau module : ".$newid[0];
                }
                else {
                    die("<strong>Erreur</strong><br>Impossible de créer un nouveau champ.<br>Veuillez vérifier la connexion et réessayez");
                }
            }
            else {
                die("<strong>Erreur</strong><br>Champ(s) manquant(s).<br>");
            }

        ?>
    </body>
</html>

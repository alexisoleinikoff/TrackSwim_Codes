<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr">

    <head>
        <meta charset="utf8">
        <title> Administrateur > Visualiser DB bracelet</title>
        <link rel="stylesheet" href="style.css">

        <!-- Script pour l'ouverture de la bannière-->
        <script src="jquery.js"></script>
        <script>
            $(function(){
                $("#includedBanner").load("banner.html"); 
            });
        </script>
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

            if (!empty($_POST['ADMIN_ADD_ID']) and !empty($_POST['ADMIN_ADD_PASS'])) {
                $bdd->query("INSERT INTO admin (Identifiant, Mot_de_passe) VALUES ('".$_POST['ADMIN_ADD_ID']."', '".$_POST['ADMIN_ADD_PASS']."')");
                $newid = $bdd->query("SELECT @@IDENTITY");
                $newid = $newid->fetch();
                if (!empty($newid) and $newid[0] != 0) {
                    echo "<strong>Succès</strong><br>Identifiant propre du nouvel administrateur : ".$newid[0];
                }
                else {
                    die("<strong>Erreur</strong><br>Impossible de créer un nouveau champ.<br>Veuillez vérifier la connexion et réessayez");
                }
            }
            else {
                die("<strong>Erreur</strong><br>Champ(s) manquant(s).");
            }
        ?>
    </body>
</html>

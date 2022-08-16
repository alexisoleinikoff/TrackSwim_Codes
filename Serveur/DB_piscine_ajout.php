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

            if (!empty($_POST['POOL_ADD_NAME']) and !empty($_POST['POOL_ADD_LOCAL']) and !empty($_POST['POOL_ADD_PC']) and !empty($_POST['POOL_ADD_CITY']) and !empty($_POST['POOL_ADD_SIZE'])) {
                $bdd->query("INSERT INTO piscine (Nom, Adresse, Code_postal, Ville, Longueur) VALUES ('".$_POST['POOL_ADD_NAME']."', '".$_POST['POOL_ADD_LOCAL']."', '".$_POST['POOL_ADD_PC']."', '".$_POST['POOL_ADD_CITY']."', '".$_POST['POOL_ADD_SIZE']."')");
                $newid = $bdd->query("SELECT @@IDENTITY");
                $newid = $newid->fetch();
                if (!empty($newid) and $newid[0] != 0) {
                    echo "<strong>Succès!</strong><br>Identifiant propre de la nouvelle piscine : ".$newid[0];
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

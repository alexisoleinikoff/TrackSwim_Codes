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

            if (!empty($_POST['ID_ADMIN_TO_DELETE'])) {
                $admins = $bdd->query("SELECT * FROM admin");
                if ($admins->rowCount() > 1) {
                    $bdd->query("DELETE FROM admin WHERE ID_admin = ".$_POST['ID_ADMIN_TO_DELETE']);
                    echo "<strong>Succès</strong><br>Administrateur ".$_POST['ID_ADMIN_TO_DELETE']." correctement supprimé.<br>
                       Si cet identifiant avait été utilisé pour se connecter, veuillez retourner à la page d'accueil et entrer un autre valable.<br><br>
                       Reste des tables non affecté";
                }
                else {
                    die("<strong>Erreur</strong><br>Limite minimale d'administrateur atteinte.<br>Veuillez en créer un autre et réessayer.");
                }
            }
            else {
                die("<strong>Erreur</strong><br>Champ(s) manquant(s).<br>");
            }
        ?>
    </body>
</html>

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

            if (!empty($_POST['ID_USER_TO_DELETE'])) {
                $listeAssoc = $bdd->query("SELECT * FROM association_utilisateur_tag WHERE ID_utilisateur = ".$_POST['ID_USER_TO_DELETE']);

                if (!empty($listeAssoc->fetch())) {
                    die("<strong>Erreur</strong><br>Impossible de supprimer cet utilisateur. Ce dernier est encore associé à un ou plusieurs bracelets.<br>
                    Veuillez supprimer ces associations et réessayer.");
                }

                $bdd->query("DELETE FROM utilisateur WHERE ID_utilisateur = ".$_POST['ID_USER_TO_DELETE']);
                
                echo "<strong>Succès</strong><br>Utilisateur ".$_POST['ID_USER_TO_DELETE']." correctement supprimé.<br>
                Reste des tables non affecté.";
            }
            else {
                die("<strong>Erreur</strong><br>Champ(s) manquant(s).<br>");
            }
        ?>
    </body>
</html>

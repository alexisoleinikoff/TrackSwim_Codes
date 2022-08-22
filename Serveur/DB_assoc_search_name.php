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

            if (!empty($_POST['ASSOC_SCH_NAME']) and !empty($_POST['ASSOC_SCH_SURNAME'])) {
                $listeUser = $bdd->query("SELECT * FROM utilisateur");
                while ($user = $listeUser->fetch()) {
                    if ($user[0] == $_POST['ASSOC_SCH_NAME'] and $user[1] == $_POST['ASSOC_SCH_SURNAME']) {
                        break;
                    }
                }

                if(!$user) {
                    die("Cet utilisateur n'a pas été trouvé dans la base de données.");
                }

                $listeAssoc = $bdd->query("SELECT * FROM association_utilisateur_tag WHERE ID_utilisateur =".$user[3]);

                if (!$listeAssoc->fetch()) {
                    die("Cet utilisateur n'est associé à aucun bracelet.");
                }
                else {
                    echo "L'utilisateur ".$user[0]." ".$user[1]." est associé au(x) bracelet(s) suivant(s) :<br><br>";
                }

                $listeAssoc = $bdd->query("SELECT * FROM association_utilisateur_tag WHERE ID_utilisateur =".$user[3]);

                while($assoc = $listeAssoc->fetch()) {
                    $listeTag = $bdd->query("SELECT * FROM tag WHERE ID_tag =".$assoc[1]);
                    # vérifier si le tag existe ici
                    $tag = $listeTag->fetch();
                    echo "[".$tag[0]."] (ID propre ".$tag[1].") → Association ".$assoc[2]."<br>";

                }

            }
            else {
                die("<strong>Erreur</strong><br>Champ(s) manquant(s).<br>");
            }

        ?>
    </body>
</html>

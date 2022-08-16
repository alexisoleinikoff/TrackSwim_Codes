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

            if (!empty($_POST['ASSOC_SCH_TAG'])) {
                $listeTag = $bdd->query("SELECT * FROM tag");
                while ($tag = $listeTag->fetch()) {
                    if ($tag[0] == $_POST['ASSOC_SCH_TAG']) { #Attention, prend uniquement le 1er tag -> pas de doublon
                        break;
                    }
                }

                if (!$tag) {
                    die("Il n'existe pas de bracelet pour cet EPC.");
                }

                $res = $bdd->query("SELECT * FROM association_utilisateur_tag WHERE ID_tag = ".$tag[1]);
                if (!($row = $res->fetch())) {
                    die("Le bracelet ayant comme EPC [".$_POST['ASSOC_SCH_TAG']."] n'est pas encore associé.");
                }
                else {
                    $res = $bdd->query("SELECT * FROM utilisateur WHERE ID_utilisateur =".$row[0]);
                    $row = $res->fetch();

                    echo "Le bracelet ayant comme EPC [".$_POST['ASSOC_SCH_TAG']."]
                    (ID propre ".$tag[1].") est associé à ".$row[0]." ".$row[1].".";
                }

            }
            else {
                die("<strong>Erreur</strong><br>Champ(s) manquant(s).<br>");
            }
        ?>
    </body>
</html>

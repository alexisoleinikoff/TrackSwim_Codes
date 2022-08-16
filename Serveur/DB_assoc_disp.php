<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr">

    <head>
        <meta charset="utf8">
        <title> Administrateur > Visualiser DB administrateur</title>
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

            try {
                $bdd = new PDO($mon_Path_BD, $mon_userName, $monPSW);
                #echo "BD ouverte <BR>";
            }
            catch (Exception $e) {
                die('Erreur : ' . $e->getMessage());
            }
        ?>

        <table border="0">
            <TR height="20">
                <TD width="250" align="left">
                    <strong>Utilisateur</strong>
                </TD>
                <TD width="150" align="left">
                    <strong>ID utilisateur</strong>
                </TD>
                <TD width="300" align="left">
                    <strong>Code produit électronique (EPC)</strong>
                </TD>
                <TD width="150" align="left">
                    <strong>ID du bracelet</strong>
                </TD>
                <TD width="150" align="left">
                    <strong>Clé d'identification</strong>
                </TD>
            </TR>

        <?php

        $listeAssoc = $bdd->query("SELECT * FROM association_utilisateur_tag ORDER BY ID_utilisateur");
        foreach($listeAssoc as $assoc) {
            $user = $bdd->query("SELECT Nom, Prenom FROM utilisateur WHERE ID_utilisateur = ".$assoc[0])->fetch();
            $tag = $bdd->query("SELECT EPC FROM tag WHERE ID_tag = ".$assoc[1])->fetch();

            echo "<TR>
                <TD>".$user[0]." ".$user[1]."</TD>
                <TD>".$assoc[0]."</TD>
                <TD>".$tag[0]."</TD>
                <TD>".$assoc[1]."</TD>
                <TD>".$assoc[2]."</TD>
                </TR>";

        }

        ?>

        </table>
    </body>
</html>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr">

    <head>
        <meta charset="utf8">
        <title> Administrateur > Visualiser DB utilisateur</title>
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
        ?>

        <table border="0">
            <TR height="20">
                <TD width="100" align="left">
                    <strong>Nom</strong>
                </TD>
                <TD width="100" align="left">
                    <strong>Prénom</strong>
                </TD>
                <TD width="200" align="left">
                    <strong>Date de naissance</strong>
                </TD>
                <TD width="200" align="left">
                    <strong>Clé d'identification</strong>
                </TD>
            </TR>


         <?php
            $personnes = $bdd->query("SELECT * FROM utilisateur");
            foreach($personnes as $unepersonne) {
                echo "<TR><TD>".$unepersonne['Nom']."</TD><TD>".$unepersonne['Prenom']."</TD><TD>".$unepersonne['Date_de_naissance']."</TD><TD>".$unepersonne['ID_utilisateur']."</TD><TD></TR>";
            }
        ?>

        </table>
    </body>
</html>
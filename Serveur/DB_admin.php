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
                <TD width="100" align="left">
                    <strong>Identifiant</strong>
                </TD>
                <TD width="100" align="left">
                    <strong>Mot de passe</strong>
                </TD>
                <TD width="200" align="left">
                    <strong>Clé d'identification</strong>
                </TD>
            </TR>

        <?php
            $admin = $bdd->query("SELECT * FROM admin");
            foreach($admin as $unadmin) {
                echo "<TR><TD>".$unadmin['Identifiant']."</TD><TD>".$unadmin['Mot_de_passe']."</TD><TD>".$unadmin['ID_admin']."</TD><TD></TR>";
            }
        ?>

        </table>
    </body>
</html>
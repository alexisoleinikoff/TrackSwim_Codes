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
        ?>

        <table border="0">
            <TR height="20">
                <TD width="300" align="left">
                    <strong>Code produit électronique (EPC)</strong>
                </TD>
                <TD width="150" align="left">
                    <strong>Clé d'identification</strong>
                </TD>
            </TR>

         <?php
            $tags = $bdd->query("SELECT * FROM tag");
            foreach($tags as $tag) {
                echo "<TR><TD>".$tag['EPC']."</TD><TD>".$tag['ID_tag']."</TD></TR>";
            }
        ?>

        </table>

    </body>
</html>
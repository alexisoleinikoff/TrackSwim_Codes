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

            if (!empty($_POST['ID_POOL_TO_DELETE'])) {
                $bdd->query("DELETE FROM piscine WHERE ID_piscine = ".$_POST['ID_POOL_TO_DELETE']);
                echo "<strong>Succès</strong><br>Piscine ".$_POST['ID_POOL_TO_DELETE']." correctement supprimée.<br>
                    Vérifiez si un ou plusieurs modules n'y étaient pas déployés. <br>Dans le cas d'une piscine non-existante,
                    la valeur de la longueur du bassin par défaut (25 mètres) est utilisée.";
            }
            else {
                die("<strong>Erreur</strong><br>Champ(s) manquant(s).<br>");
            }
        ?>
    </body>
</html>

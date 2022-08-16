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

            if (!empty($_POST['ID_MODULE_TO_UPDATE'])) {
                $bool_mode = False;
                $bool_pool = False;

                $module = $bdd->query("SELECT * FROM module WHERE ID_module = ".$_POST['ID_MODULE_TO_UPDATE']);
                
                if(!($module = $module->fetch())) {
                    die("<strong>Erreur</strong><br>Le module dont l'ID propre est ".$_POST['ID_MODULE_TO_UPDATE']." n'existe pas.");
                }


                if(empty($_POST['MODE_MODULE_TO_UPDATE']) or $_POST['MODE_MODULE_TO_UPDATE'] == $module[0]) {
                    $mode_update = $module[0];
                }
                else {
                    $mode_update = $_POST['MODE_MODULE_TO_UPDATE'];
                    $bool_mode = True;
                }

                if(empty($_POST['POOL_MODULE_TO_UPDATE']) or $_POST['POOL_MODULE_TO_UPDATE'] == $module[1]) {
                    $pool_update = $module[1];
                }
                else {
                    $pool_update = $_POST['POOL_MODULE_TO_UPDATE'];
                    $bool_pool = True;
                }

                $bdd->query("UPDATE module SET Mode = '".$mode_update."', ID_piscine = '".$pool_update."' WHERE ID_module = ".$_POST['ID_MODULE_TO_UPDATE']);
                if ($bool_mode or $bool_pool) {
                    echo "<strong>Succès</strong><br>Les champs suivant ont été modifiés pour le module dont l'ID propre est ". $_POST['ID_MODULE_TO_UPDATE'] ." : <br><br>";
                    if ($bool_mode) {
                        echo "Mode : ".$module[0]." → ".$_POST['MODE_MODULE_TO_UPDATE']."<br>";
                    }

                    if ($bool_pool) {
                        echo "ID Piscine : ".$module[1]." → ".$_POST['POOL_MODULE_TO_UPDATE']."<br>";
                    }

                }
                else {
                    echo "<strong>Succès</strong><br>Aucun champ n'a dû être mis à jour pour le module dont l'ID propre est ". $_POST['ID_MODULE_TO_UPDATE'] .".<br>";
                }
                
                
            }
            else {
                die("<strong>Erreur</strong><br>Champ(s) manquant(s).<br>");
            }

        ?>
    </body>
</html>

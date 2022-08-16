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


            if (!empty($_POST['USER_SCH_NAME']) and !empty($_POST['USER_SCH_SURNAME'])) {
                $listeUser = $bdd->query("SELECT * FROM utilisateur");
                while ($user = $listeUser->fetch()) {
                    if ($user[0] == $_POST['USER_SCH_NAME'] and $user[1] == $_POST['USER_SCH_SURNAME']) {
                        die("L'utilisateur [".$_POST['USER_SCH_NAME']." ".$_POST['USER_SCH_SURNAME']."] porte l'indice d'identification ".$user[3]);
                    }
                }
                die("Cet utilisateur n'a pas été trouvé dans la base de données.");

            }
            else {
                die("<strong>Erreur</strong><br>Champ(s) manquant(s).");
            }

        ?>
    </body>
</html>

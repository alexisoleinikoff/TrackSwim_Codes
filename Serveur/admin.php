<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr">

    <head>
        <meta charset="utf8">
        <title> Home > Administrateur</title>
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

            # Vérification de la connexion et récupération de l'ID de l'administrateur
            if($_POST['ADMIN_NAME']) {
                $ADMIN_NAME = $_POST['ADMIN_NAME'];
                $ADMIN_PASS = $_POST['ADMIN_PASS'];
            }
            else {
                die("<strong>Connexion erronnée</strong>.<br> Veuillez vérifier votre identifiant et/ou mot de passe (code : 2) <BR>");
            }

            $result = $bdd->query("SELECT ID_admin FROM admin WHERE Identifiant='".$ADMIN_NAME."' AND Mot_de_passe='".$ADMIN_PASS."'");
            if ($row = $result->fetch()) {
                echo "Connexion OK. ID de l'administrateur actuellement connecté : ";
                echo $row['ID_admin'];
                echo "<BR>";
            }
            else {
                die("<strong>Connexion erronnée</strong>.<br> Veuillez vérifier votre identifiant et/ou mot de passe (code : 1) <BR>");
            }
            ?>

            <table border="0">
                <TR height="20">
                    <TD width="1500" colspan="2" align="left">
                        <h2>> Gestion des utilisateurs</h2>
                    </TD>
                </TR>
                <TR height="40">
                    <TD width="50" colspan="1" align="left">
                        <!-- Laisser vide pour retrait -->
                    </TD>
                    <TD colspan="1" align="left">
                        <a href ="DB_utilisateur.php">Visualiser la base de donnée des utilisateurs</a><br><br>
                        <a href ="DB_utilisateur.php">Ajouter un nouvel utilisateur</a><br><br>
                        <a href ="DB_utilisateur.php">Supprimer un utilisateur</a>
                    </TD>
                </TR>
                <TR height="20">
                    <TD width="1500" colspan="2" align="left">
                        <h2>> Gestion des administrateurs</h2>
                    </TD>
                </TR>
                <TR height="40">
                    <TD width="50" colspan="1" align="left">
                        <!-- Laisser vide pour retrait -->
                    </TD>
                    <TD colspan="1" align="left">
                        <a href ="DB_admin.php">Visualiser la base de donnée des administrateurs</a><br><br>
                        <a href ="DB_admin.php">Ajouter un nouvel administrateur</a><br><br>
                        <a href ="DB_admin.php">Supprimer un administrateur</a>
                    </TD>
                </TR>
                <TR height="20">
                    <TD width="1500" colspan="2" align="left">
                        <h2>> Gestion des piscines</h2>
                    </TD>
                </TR>
                <TR height="40">
                    <TD width="50" colspan="1" align="left">
                        <!-- Laisser vide pour retrait -->
                    </TD>
                    <TD colspan="1" align="left">
                        <a href ="DB_piscine.php">Visualiser la base de donnée des piscines</a><br><br>
                        <a href ="DB_piscine.php">Ajouter une nouvelle piscine</a><br><br>
                        <a href ="DB_piscine.php">Supprimer une piscine</a>
                    </TD>
                </TR>
                <TR height="20">
                    <TD width="1500" colspan="2" align="left">
                        <h2>> Gestion des bracelets</h2>
                    </TD>
                </TR>
                <TR height="40">
                    <TD width="50" colspan="1" align="left">
                        <!-- Laisser vide pour retrait -->
                    </TD>
                    <TD colspan="1" align="left">
                        <a href ="DB_tag.php">Visualiser la base de donnée des bracelets connectés</a><br><br>
                        <a href ="DB_tag.php">Ajouter un nouveau bracelet connecté</a><br><br>
                        Attribuer un bracelet à un utilisateur<br><br>
                        Supprimer l'attribution d'un bracelet à un utilisateur
                    </TD>
                </TR>
            </table>

        <BR>

    </body>
</html>
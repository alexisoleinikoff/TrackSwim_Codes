<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr">
    <head>
        <meta charset="utf8">
        <title> Bienvenu sur TrackSwim!</title>
        <link rel="stylesheet" href="style.css"/>

        <!-- Script pour l'ouverture de la bannière-->
        <script src="jquery.js"></script>
        <script>
            $(function(){
                $("#includedBanner").load("banner.html"); 
            });
        </script>
    </head>

    <body>

        <!-- Connexion à la base de données -->
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

        <!-- Bannière -->
        <div id="includedBanner"></div>
        
        <!-- Body -->
        <center>
        <table border="0">
            <TR heigth="1000">
                <TD width="500" colspan="2" align="center">
                    <h2>Utilisateur</h2><hr>
                </TD>

                <TD width="100" align="center">
                    
                </TD>

                <TD width="100" align="center">
                    
                </TD>

                <TD width="500" colspan="2" align="center">
                    <h2>Administateur</h2><hr>
                </TD>
            </TR>

            <TR>
                <TD align="center">
                    Identifiant <BR><BR>Date de la session<BR><BR> <BR>
                </TD>
                <form name="userForm" action="user.php" method="POST">
                    <TD width="250" align="center" >
                        <SELECT name="ID_USER">
                            <?php
                                $listePersonnes = $bdd->query("SELECT ID_utilisateur, Nom, Prenom FROM utilisateur ORDER BY ID_utilisateur ASC");

                                while($row = $listePersonnes->fetch()) {
                                    echo "<OPTION value='".$row['ID_utilisateur']."'>".$row['Nom']." ".$row['Prenom']."</OPTION>";
                                }
                            ?>
                        <SELECT> <BR><BR>
                        <input type="date" name="SESSION_DATE"/> <BR><BR>
                        <input type="submit" value="Rechercher" />
                    </TD>
                </form>

                <TD>
                    <!-- Vide (centre) -->
                </TD>

                <TD>
                    <!-- Vide (centre) -->
                </TD>

                <TD align="center">
                    Identifiant<BR><BR>Mot de passe<BR><BR> <BR>
                </TD>

                <form name="adminForm" action="admin.php" method="POST">
                    <TD width="250" align="center">
                        <input type="text" placeholder="Identifiant" name="ADMIN_NAME" /> <BR><BR>
                        <input type="text" placeholder="Mot de passe" name="ADMIN_PASS"/> <BR><BR>
                        <input type="submit" value="Se connecter" />
                    </TD>
                </form>
            </TR>
        </table> <br><br><br><br><br><br>
        <a href="about.php">À propos de TrackSwim</a>
        


    </body>


<html>
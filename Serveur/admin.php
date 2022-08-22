<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr">

    <head>
        <meta charset="utf8">
        <title>Home > Administrateur</title>
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

            try {
                $bdd = new PDO($mon_Path_BD, $mon_userName, $monPSW);
                #echo "BD ouverte <BR>";
            }
            catch (Exception $e) {
                die('Erreur : ' . $e->getMessage());
            }

            # Vérification de la connexion et récupération de l'ID de l'administrateur
            if(!empty($_POST['ADMIN_NAME']) and !empty($_POST['ADMIN_PASS'])) {
                $ADMIN_NAME = $_POST['ADMIN_NAME'];
                $ADMIN_PASS = $_POST['ADMIN_PASS'];
            }
            else {
                die("<strong>Erreur</strong><br>Champ(s) manquant(s).<br>");
            }

            $result = $bdd->query("SELECT ID_admin FROM admin WHERE Identifiant='".$ADMIN_NAME."' AND Mot_de_passe='".$ADMIN_PASS."'");
            if ($row = $result->fetch()) {
                echo "Identifiant de l'administrateur actuellement connecté : ";
                echo $row['ID_admin'];
                echo "<BR>";
                echo "Si certaines des informations affichées ne paraissent pas à jour, veuillez rafraîchir la page.<br>";
            }
            else {
                die("<strong>Connexion erronnée</strong><br>Veuillez vérifier votre identifiant et/ou mot de passe<br>");
            }
            ?>

            <table border="0">
                <TR height="20">
                    <TD width="1500" colspan="2" align="left">
                        <h2>Gestion des utilisateurs <a href="DB_user_disp.php"><img src="Media\eye.png" alt="Visualiser la tables des utilisateurs" width="30"></a></h2>
                    </TD>
                </TR>
                <TR height="40">
                    <TD width="50" colspan="1" align="left">
                        <!-- Laisser vide pour retrait -->
                    </TD>
                    <form name="addUserForm" action="DB_user_ajout.php" method="POST">
                        <TD colspan="1" align="left">
                            Ajouter un nouvel utilisateur : &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp <!-- &nbsp = espace -->
                            <input type="text" placeholder="Nom" name="USER_ADD_NAME"/> &nbsp&nbsp&nbsp
                            <input type="text" placeholder="Prénom" name="USER_ADD_SURNAME"/> &nbsp&nbsp&nbsp
                            <input type="date" placeholder="Date de naissance" name="USER_ADD_DOB"/> &nbsp&nbsp&nbsp
                            <input type="submit" value="Ajouter"/>
                        </TD>
                    </form>
                </TR>
                <TR height="40">
                    <TD width="50" colspan="1" align="left">
                        <!-- Laisser vide pour retrait -->
                    </TD>
                    <form name="schUserForm" action="DB_user_search.php" method="POST">
                        <TD colspan="1" align="left">
                            Chercher l'ID d'un utilisateur : &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp <!-- &nbsp = espace -->
                            <input type="text" placeholder="Nom" name="USER_SCH_NAME"/> &nbsp&nbsp&nbsp
                            <input type="text" placeholder="Prénom" name="USER_SCH_SURNAME"/> &nbsp&nbsp&nbsp
                            <input type="submit" value="Chercher"/>
                        </TD>
                    </form>
                </TR>
                <TR height="40">
                    <TD width="50" colspan="1" align="left">
                        <!-- Laisser vide pour retrait -->
                    </TD>
                    <form name="delUserForm" action="DB_user_supp.php" method="POST">
                        <TD colspan="1" align="left">
                            Supprimer un utilisateur : &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
                            <SELECT name="ID_USER_TO_DELETE">
                                <OPTION value='' disabled selected>Utilisateur</OPTION>
                                <?php
                                    $listePersonnes = $bdd->query("SELECT ID_utilisateur, Nom, Prenom FROM utilisateur ORDER BY ID_utilisateur ASC");

                                    while($row = $listePersonnes->fetch()) {
                                        echo "<OPTION value='".$row['ID_utilisateur']."'>".$row['Nom']." ".$row['Prenom']."</OPTION>";
                                    }
                                ?>
                            </SELECT>&nbsp&nbsp&nbsp
                            <input type="submit" value="Supprimer"/>
                        </TD>
                    </form>
                </TR>
                


                <TR height="20">
                    <TD width="1500" colspan="2" align="left">
                        <h2>Gestion des bracelets <a href="DB_tag_disp.php"><img src="Media\eye.png" alt="Visualiser la tables des bracelets" width="30"></a></h2>
                    </TD>
                </TR>
                <TR height="40">
                    <TD width="50" colspan="1" align="left">
                        <!-- Laisser vide pour retrait -->
                    </TD>
                    <form name="addTagForm" action="DB_tag_ajout.php" method="POST">
                        <TD colspan="1" align="left">
                            Ajouter un nouveau bracelet : &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
                            <input type="text" placeholder="EPC format : b'E00...'" name="TAG_ADD_EPC"/> &nbsp&nbsp&nbsp
                            <input type="submit" value="Ajouter"/>
                        </TD>
                    </form>
                </TR>
                <TR height="40">
                    <TD width="50" colspan="1" align="left">
                        <!-- Laisser vide pour retrait -->
                    </TD>
                    <form name="schTagForm" action="DB_tag_search.php" method="POST">
                        <TD colspan="1" align="left">
                            Chercher l'ID d'un bracelet : &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
                            <input type="text" placeholder="EPC format : b'E00...'" name="TAG_SCH_EPC"/> &nbsp&nbsp&nbsp
                            <input type="submit" value="Chercher"/>
                        </TD>
                    </form>
                </TR>

                <TR height="20">
                    <TD width="1500" colspan="2" align="left">
                        <h2>Gestion des associations <a href="DB_assoc_disp.php"><img src="Media\eye.png" alt="Visualiser la tables des associations" width="30"></a></h2>
                    </TD>
                </TR>
                <TR height="40">
                    <TD width="50" colspan="1" align="left">
                        <!-- Laisser vide pour retrait -->
                    </TD>
                    <form name="addAssocForm" action="DB_assoc_ajout.php" method="POST">
                        <TD colspan="1" align="left">
                            Ajouter une nouvelle association :
                            <input type="number" placeholder="ID Utilisateur" name="ASSOC_ADD_ID_USER" min="1"/> &nbsp&nbsp&nbsp
                            <input type="number" placeholder="ID Bracelet" name="ASSOC_ADD_ID_TAG" min="1"/> &nbsp&nbsp&nbsp
                            <input type="submit" value="Ajouter"/>
                        </TD>
                    </form>
                </TR>
                <TR height="40">
                    <TD width="50" colspan="1" align="left">
                        <!-- Laisser vide pour retrait -->
                    </TD>
                    <form name="sch1AssocForm" action="DB_assoc_search_name.php" method="POST">
                        <TD colspan="1" align="left">
                            Chercher une association : &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
                            <input type="text" placeholder="Nom" name="ASSOC_SCH_NAME"/> &nbsp&nbsp&nbsp
                            <input type="text" placeholder="Prénom" name="ASSOC_SCH_SURNAME"/> &nbsp&nbsp&nbsp
                            <input type="submit" value="Chercher"/>
                        </TD>
                    </form>
                </TR>
                <TR height="40">
                    <TD width="50" colspan="1" align="left">
                        <!-- Laisser vide pour retrait -->
                    </TD>
                    <form name="sch2AssocForm" action="DB_assoc_search_tag.php" method="POST">
                        <TD colspan="1" align="left">
                            Chercher une association : &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
                            <input type="text" placeholder="EPC format : b'E00...'" name="ASSOC_SCH_TAG"/> &nbsp&nbsp&nbsp
                            <input type="submit" value="Chercher"/>
                        </TD>
                    </form>
                </TR>
                <TR height="40">
                    <TD width="50" colspan="1" align="left">
                        <!-- Laisser vide pour retrait -->
                    </TD>
                    <form name="suppAssocForm" action="DB_assoc_supp.php" method="POST">
                        <TD colspan="1" align="left">
                            Supprimer une association : &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
                            <input type="number" placeholder="ID Association" name="ID_ASSOC_TO_DELETE" min="1"/> &nbsp&nbsp&nbsp
                            <input type="submit" value="Supprimer"/>
                        </TD>
                    </form>
                </TR>



                <TR height="20">
                    <TD width="1500" colspan="2" align="left">
                        <h2>Gestion des modules <a href="DB_module_disp.php"><img src="Media\eye.png" alt="Visualiser la tables des modules" width="30"></a></h2>
                    </TD>
                </TR>
                <TR height="40">
                    <TD width="50" colspan="1" align="left">
                        <!-- Laisser vide pour retrait -->
                    </TD>
                    <form name="addModuleForm" action="DB_module_ajout.php" method="POST">
                        <TD>
                            Ajouter un nouveau module : &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
                            <SELECT name="MODULE_TO_ADD_MODE">
                                <OPTION value='' disabled selected>Mode</OPTION>
                                <OPTION value='Pause'>Pause</OPTION>
                                <OPTION value='Continu'>Continu</OPTION>
                            </SELECT> &nbsp&nbsp&nbsp
                            <SELECT name="MODULE_TO_ADD_POOL">
                                <OPTION value='' disabled selected>Piscine</OPTION>
                                <?php
                                    $listePiscine = $bdd->query("SELECT ID_piscine, Nom, Ville FROM piscine ORDER BY ID_piscine ASC");

                                    while($row = $listePiscine->fetch()) {
                                        echo "<OPTION value='".$row['ID_piscine']."'>".$row['Nom'].", ".$row['Ville']."</OPTION>";
                                    }
                                ?>
                            </SELECT>&nbsp&nbsp&nbsp
                            <input type="submit" value="Ajouter"/>
                        </TD>
                    </form>
                </TR>
                <TR height="40">
                    <TD width="50" colspan="1" align="left">
                        <!-- Laisser vide pour retrait -->
                    </TD>
                    <form name="upModuleForm" action="DB_module_update.php" method="POST">
                        <TD>
                            Modifier un module existant : &nbsp&nbsp&nbsp&nbsp&nbsp
                            <input type="number" placeholder="ID Module" name="ID_MODULE_TO_UPDATE" min="1"/> &nbsp&nbsp&nbsp
                            <SELECT name="MODE_MODULE_TO_UPDATE">
                                <OPTION value='' disabled selected>Mode</OPTION>
                                <OPTION value='Pause'>Pause</OPTION>
                                <OPTION value='Continu'>Continu</OPTION>
                            </SELECT> &nbsp&nbsp&nbsp
                            <SELECT name="POOL_MODULE_TO_UPDATE">
                                <OPTION value='' disabled selected>Piscine</OPTION>
                                <?php
                                    $listePiscine = $bdd->query("SELECT ID_piscine, Nom, Ville FROM piscine ORDER BY ID_piscine ASC");

                                    while($row = $listePiscine->fetch()) {
                                        echo "<OPTION value='".$row['ID_piscine']."'>".$row['Nom'].", ".$row['Ville']."</OPTION>";
                                    }
                                ?>
                            </SELECT>&nbsp&nbsp&nbsp
                            <input type="submit" value="Modifier"/>

                        </TD>
                    </form>
                </TR>
                <!-- 
                <TR height="40">
                    <TD width="50" colspan="1" align="left">
                        Laisser vide pour retrait
                    </TD>
                    <form name="suppModuleForm" action="DB_module_supp.php" method="POST">
                        <TD>
                            Supprimer un module : &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
                            <input type="number" placeholder="ID Module" name="ID_MODULE_TO_DELETE" min="1"/> &nbsp&nbsp&nbsp
                            <input type="submit" value="Supprimer">
                        </TD>
                    </form>
                </TR> -->


                <TR height="20">
                    <TD width="1500" colspan="2" align="left">
                        <h2>Gestion des piscines <a href="DB_piscine_disp.php"><img src="Media\eye.png" alt="Visualiser la tables des piscines" width="30"></a></h2>
                    </TD>
                </TR>
                <TR height="40">
                    <TD width="50" colspan="1" align="left">
                        <!-- Laisser vide pour retrait -->
                    </TD>
                    <form name="addPoolForm" action="DB_piscine_ajout.php" method="POST">
                        <TD colspan="1" align="left">
                            Ajouter une nouvelle piscine : &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp   
                            <input type="text" placeholder="Nom" name="POOL_ADD_NAME"/> &nbsp&nbsp&nbsp
                            <input type="text" placeholder="Adresse" name="POOL_ADD_LOCAL"/> &nbsp&nbsp&nbsp
                            <input type="text" placeholder="Code postal" name="POOL_ADD_PC"/> &nbsp&nbsp&nbsp
                            <input type="text" placeholder="Ville" name="POOL_ADD_CITY"/> &nbsp&nbsp&nbsp
                            <input type="number" placeholder="Longueur du bassin" name="POOL_ADD_SIZE" min='12'/> &nbsp&nbsp&nbsp
                            <input type="submit" value="Ajouter"/>
                        </TD>
                    </form>
                </TR>
                <TR height="40">
                    <TD width="50" colspan="1" align="left">
                        <!-- Laisser vide pour retrait -->
                    </TD>
                    <form name="delPoolForm" action="DB_piscine_supp.php" method="POST">
                        <TD colspan="1" align="left">
                            Supprimer une piscine : &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
                            <SELECT name="ID_POOL_TO_DELETE">
                                <OPTION value='' disabled selected>Piscine</OPTION>
                                <?php
                                    $listePiscine = $bdd->query("SELECT ID_piscine, Nom, Ville FROM piscine ORDER BY ID_piscine ASC");

                                    while($row = $listePiscine->fetch()) {
                                        echo "<OPTION value='".$row['ID_piscine']."'>".$row['Nom'].", ".$row['Ville']."</OPTION>";
                                    }
                                ?>
                            </SELECT>&nbsp&nbsp&nbsp
                            <input type="submit" value="Supprimer"/>
                        </TD>
                    </form>
                </TR>



                <TR height="20">
                    <TD width="1500" colspan="2" align="left">
                        <h2>Gestion des administrateurs <a href="DB_admin_disp.php"><img src="Media\eye.png" alt="Visualiser la tables des administrateurs" width="30"></a></h2>
                    </TD>
                </TR>
                <TR height="40">
                    <TD width="50" colspan="1" align="left">
                        <!-- Laisser vide pour retrait -->
                    </TD>
                    <form name="addAdminForm" action="DB_admin_ajout.php" method="POST">
                        <TD colspan="1" align="left">
                            Ajouter un nouvel administrateur :
                            <input type="text" placeholder="Identifiant" name="ADMIN_ADD_ID"/> &nbsp&nbsp&nbsp
                            <input type="text" placeholder="Mot de passe" name="ADMIN_ADD_PASS"/> &nbsp&nbsp&nbsp
                            <input type="submit" value="Ajouter"/>
                        </TD>
                    </form>
                </TR>
                <TR height="40">
                    <TD width="50" colspan="1" align="left">
                        <!-- Laisser vide pour retrait -->
                    </TD>
                    <form name="delAdminForm" action="DB_admin_supp.php" method="POST">
                        <TD colspan="1" align="left">
                            Supprimer un administrateur : &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
                            <SELECT name="ID_ADMIN_TO_DELETE">
                                <OPTION value='' disabled selected>Administrateur</OPTION>
                                <?php
                                    $listeAdmin = $bdd->query("SELECT ID_admin, Identifiant FROM admin ORDER BY ID_admin ASC");

                                    while($row = $listeAdmin->fetch()) {
                                        echo "<OPTION value='".$row['ID_admin']."'>".$row['Identifiant']."</OPTION>";
                                    }
                                ?>
                            </SELECT>&nbsp&nbsp&nbsp
                            <input type="submit" value="Supprimer"/>
                        </TD>
                    </form>
                </TR>
            </table>
        <BR>
    </body>
</html>
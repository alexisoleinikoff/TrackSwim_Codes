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

            if (!empty($_POST['ASSOC_ADD_ID_USER']) and !empty($_POST['ASSOC_ADD_ID_TAG'])) {
                $i = 0;
                $listeTag = $bdd->query("SELECT * FROM tag WHERE ID_tag = ".$_POST['ASSOC_ADD_ID_TAG']);
                if (!($tag = $listeTag->fetch())) {
                    die("<strong>Erreur</strong><br>Aucun bracelet n'existe pour l'identifiant propre ".$_POST['ASSOC_ADD_ID_TAG']);
                }

                # Vérifie si le tag n'est pas déjà associé
                $listeAssoc = $bdd->query("SELECT * FROM association_utilisateur_tag WHERE ID_tag = ".$_POST['ASSOC_ADD_ID_TAG']);
                while ($assoc = $listeAssoc->fetch()) {
                    $i++;
                }

                # Si un tag est déjà associé, quitter le programme
                if ($i != 0) {
                    $listeAssoc = $bdd->query("SELECT * FROM association_utilisateur_tag WHERE ID_tag = ".$_POST['ASSOC_ADD_ID_TAG']);
                    $assoc = $listeAssoc->fetch();

                    $assocUser = $bdd->query("SELECT Nom, Prenom FROM utilisateur WHERE ID_utilisateur = ".$assoc[0]);
                    $assocUser = $assocUser->fetch();

                    die("<strong>Erreur</strong><br>Le bracelet portant l'indice
                    d'identification ".$_POST['ASSOC_ADD_ID_TAG']." a déjà été attribué à un autre utilisateur.<br>
                    Association actuelle avec : ".$assocUser['Nom']." ".$assocUser['Prenom']." (ID de l'association : ".$assoc[2].").<br><br>
                    Veuillez d'abord supprimer cette association, puis réessayer.");
                }

                # Vérifier si utilisateur existe
                $user = $bdd->query("SELECT * FROM utilisateur WHERE ID_utilisateur = ".$_POST['ASSOC_ADD_ID_USER']);
                if (!($user->fetch())) {
                    die("<strong>Erreur</strong><br>Aucun utilisateur n'existe pour l'identifiant propre ".$_POST['ASSOC_ADD_ID_USER']);
                }


                # Si tout ok, -> associer
                $bdd->query("INSERT INTO association_utilisateur_tag (ID_utilisateur, ID_tag) VALUES ('".$_POST['ASSOC_ADD_ID_USER']."', '".$_POST['ASSOC_ADD_ID_TAG']."')");
                $newid = $bdd->query("SELECT @@IDENTITY");
                $newid = $newid->fetch();
                if (!empty($newid) and $newid[0] != 0) {
                    echo "<strong>Succès</strong><br>Identifiant propre de la nouvelle association : ".$newid[0];
                }
                else {
                    die("<strong>Erreur</strong><br>Impossible de créer un nouveau champ.<br>Veuillez vérifier la connexion et réessayez");
                }



            }
            else {
                die("<strong>Erreur</strong><br>Champ(s) manquant(s).<br>");
            }


        ?>
    </body>
</html>

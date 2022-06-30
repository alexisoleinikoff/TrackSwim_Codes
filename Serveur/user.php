<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr">

    <head>
        <meta charset="utf8">
        <title> Home > Utilisateur</title>
        <link rel="stylesheet" href="style.css">


        <!-- Script pour les graphiques-->
        <script src="chart.js"></script>

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
        
            if($_POST['SESSION_DATE']) {
                $SESSION_DATE = $_POST['SESSION_DATE'];
                $USER_ID = $_POST['ID_USER'];
                $x = array();
                $y = array();
                $i = 0;
                $j = 1;
               # $tagAmm = 0;
                $sessionAmm = 0;
                $stringx = "var xValues = [";
                $stringy = "var yValues = [";
            }
            else {
                die("Erreur, date de session entrée non valide (code : 3)");
            }

            echo "<h1>Sessions de natation du ".$SESSION_DATE."</h1><BR>";
            echo "<strong>Axe horizontal</strong> → Numéro de l'aller-retour [-]<BR>
                <strong>Axe vertical</strong> → Durée de l'aller-retour [s]";

            # récupération des données des performances en faisant tout le cheminement des BD
            # Ordre : Tags -> Sessions -> Performances

            # A DEVELOPPER :
            # Enlever les tags! à la place, chercher avec le ID_user seulement
            # Modifier la DB pour afficher le ID_user dans une session et non pas le ID_tag
            # tag <-> user <-> session <-> perf
            # table associative pour linker les tags et user

            $sessions = $bdd->query("SELECT ID_session FROM session WHERE ID_user=".$USER_ID." AND Debut=\"".$SESSION_DATE."\"");
            if ($sessions) {
                foreach ($sessions as $session) {
                    # Récupération ID piscine pour déterminer la longueur totale nagée
                    $pools = $bdd->query("SELECT ID_piscine FROM session WHERE ID_session=".$session["ID_session"]."");
                    $pool = $pools->fetch();
                    $pools = $bdd->query("SELECT Longueur FROM piscine WHERE ID_piscine=".$pool["ID_piscine"]."");
                    $pool = $pools->fetch();

                    # Récupération des allers-retours pour cette session
                    $perfs = $bdd->query("SELECT Depart, Arrivee FROM perf WHERE ID_session=".$session["ID_session"]." ORDER BY ID_perf");
                    if ($perfs) {
                        # Construction des variables pour le graphique
                        foreach ($perfs as $perf) {
                            $x[$i] = $i+1;
                            $stringx .= $x[$i].",";
                            $y[$i] = $perf["Arrivee"] - $perf["Depart"];
                            $stringy .= $y[$i].",";
                            $i++;
                        }
                        # Terminer le string pour graphique
                        $stringx .= "];";
                        $stringy .= "];";

                        # Construction du graphique
                        echo "<h2>Session ".$j."</h2>";
                        echo "<canvas id=\"Graphique ".$j."\" style=\"width:100%;max-width:600px\"></canvas>";
                        echo "Distance totale nagée : <strong>".(2*$i*$pool["Longueur"])." mètres</strong><br><br>";

                        echo "<script>";
                        echo "$stringx";
                        echo "$stringy";

                        echo "new Chart(\"Graphique ".$j."\", {
                            type: \"line\",
                            data: {
                                labels: xValues,
                                datasets: [{
                                fill: false,
                                lineTension: 0,
                                backgroundColor: \"rgba(0,0,255,1.0)\",
                                borderColor: \"rgba(0,0,255,0.1)\",
                                data: yValues
                                }]
                            },
                            options: {
                                legend: {display: false},
                                scales: {
                                yAxes: [{ticks: {min: 0, max: ".(max($y))."}}],
                                }
                            }
                            });
                        </script>";

                        # reset pour prochain tableau
                        $x = array();
                        $y = array();
                        $stringx = "var xValues = [";
                        $stringy = "var yValues = [";
                        $i = 0;
                        $j++;

                    }
                    else {
                        die("Aucun aller-retour trouvé pour ces sessions");
                    }

                    $sessionAmm++;
                }
            }
            else {
                die("Aucune session trouvée pour cet utilisateur à cette date");
            }

            #echo "<br><br>Nombre de tag : ".$tagAmm."<BR>";
            echo "<br><br>Nombre de session : ".$sessionAmm."<BR>";
        ?>

        </table>
    </body>
</html>
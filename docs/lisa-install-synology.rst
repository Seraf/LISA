.. _lisa-install-synology:

LISA-server on Synology NAS:
===========================
1) Mise en place de Debian:
^^^^^^^^^^^^^^^^^^^^^^^^^^

Il va nous falloir une Debian qui tourne quelque part pour générer un système de base. Si vous n’en avez pas, vous pouvez l’installer dans une machine virtuelle le temps de faire la manip (Debian net-install et Virtualbox font très bien l’affaire). Un fois ceci fait, on va utiliser debootstrap de nous générer une archive minimale pour notre architecture cible, l’ARM : 

:: 

    sudo apt-get install debootstrap  
    mkdir sdebian
    sudo debootstrap --foreign --arch armel squeeze sdebian
    sudo tar -cvzfp sdebian.tar.gz sdebian
 
Transférez l’archive obtenue sur votre NAS, placez la dans /volume1/, connectez vous au NAS grâce à telnet et désarchivez la :
:: 

    cd /volume1
    tar -xvzfp sdebian.tar.gz
 
2) Mise en place du chroot
^^^^^^^^^^^^^^^^^^^^^^^^^^

Debian aura besoin de faire des appels au noyau linux du DSM. Nous allons donc rendre accessible dans le chroot les répertoires spéciaux comme /proc, /dev …

On va utiliser un petit script shell qui va nous permettre de faire les quelques opérations nécessaires et d’entrer dans le chroot. Éditez un fichier chroot.sh, et copiez y les commandes suivantes:

:: 

    CHROOT=/volume1/sdebian
    mount -o bind /dev $CHROOT/dev
    mount -o bind /proc $CHROOT/proc
    mount -o bind /dev/pts $CHROOT/dev/pts
    mount -o bind /sys $CHROOT/sys

    cp /etc/resolv.conf $CHROOT/etc/resolv.conf
 
    chroot $CHROOT /bin/bash
    
Executez le en root, et vous serez dans le chroot. Il reste maintenant à finaliser l’installation de Debian :

/debootstrap/debootstrap --second-stage
Générez un fichier sources.list correct grâce à http://debgen.simplylinux.ch, et placez le dans /etc/apt/sources.list.

Une petite mise à jour de Debian:

::

    apt-get update
    apt-get upgrade
    
Ajout d’un compte utilisateur:

::

    adduser lisa
    
J’ai du corriger quelques droits d’accès qui se sont perdus dans la bataille. Il y en a probablement d’autres, à vous de corriger si nécessaire.
::

    chmod 777 /tmp
    chmod +t /tmp
    
Installation du minimum vital:
::

    apt-get install openssh-server htop most uptimed screen irssi
    
Pour que la Debian soit fonctionnelle, il faut maintenant faire tourner un certain nombre de services. Sur une Debian normale, ces services sont lancés par init, mais ce n’est pas notre cas. Il faudra donc les lancer manuellement. Éditez un fichier services.sh que vous placerez dans votre $HOME, et placez y le contenu suivant :

::

    /etc/init.d/rsyslog start
    /etc/init.d/mtab.sh start
    /etc/init.d/cron start
    /etc/init.d/ssh start
    /etc/init.d/uptimed start


Il faur maintenant automatiser le lancement de ce script au lancement du NAS, pour ce faire nous allons créer un fichier S99chroot.sh qui sera positionné dans le 
/usr/syno/etc/rc.d et qui lancement le script services.sh au travers de la commande chroot

contenu du fichier S99chroot.sh
::
    CHROOT=/volume1/sdebian
    mount -o bind /dev $CHROOT/dev
    mount -o bind /proc $CHROOT/proc
    mount -o bind /dev/pts $CHROOT/dev/pts
    mount -o bind /sys $CHROOT/sys

    cp /etc/resolv.conf $CHROOT/etc/resolv.conf

    chroot $CHROOT sh /home/lisa/services.sh
    
Il faut maintenant rendre ce script executable en lancement la commande:

::

    chmod +x /usr/syno/etc/rc.d/S99chroot.sh
    
Et voilà, votre Debian est fonctionnelle ! Vous avez virtuellement deux systèmes qui tournent en parallèle.

Vous pouvez maintenant passer a l'étape d'installation de lisa.

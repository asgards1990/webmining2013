//{% load static %}

function loadChargement(nomDuCadre){
  
	var loader=document.createElement("div");
	loader.id="loaderProvisoire";
	loader.style.cssText='position:relative;width:300px;height:100%;margin:0 auto'
	document.getElementById(nomDuCadre).appendChild(loader);
	var image=document.createElement("img");
	image.id="bandeauLoader";
	image.src="../pesto/static/img/explore/bandecine3.jpg";
	image.onload=function(){
	image.style.cssText='position:absolute;top:40%;left:0%;width:100%;height:20%;z-index:1;'
	document.getElementById("loaderProvisoire").appendChild(image);
	var cache=new Array;
	var position=new Array;
	position[0]=0.7;position[1]=7.75;position[2]=14.9;position[3]=22;position[4]=29;position[5]=36.1;
	position[6]=43.05;position[7]=50.4;position[8]=57.4;position[9]=64.5;position[10]=71.6;position[11]=78.7;
	position[12]=85.8;position[13]=92.8;
	var largeur=new Array;
	largeur[0]=5.8;largeur[1]=6;largeur[2]=5.9;largeur[3]=5.9;largeur[4]=6;largeur[5]=6;
	largeur[6]=6;largeur[7]=5.8;largeur[8]=6;largeur[9]=6;largeur[10]=6;largeur[11]=6;
	largeur[12]=6;largeur[13]=6;
	for(var i =0; i<14;i++){	
		cache[i]=document.createElement("div");
		cache[i].id="cache"+i;
		cache[i].style.cssText='position:absolute;top:43.5%;left:'+position[i]+'%;width:'+largeur[i]+'%;height:12.8%;z-index:2;background-color:#b0c4de;'//'+(i+1+i*6)+'
		document.getElementById("loaderProvisoire").appendChild(cache[i]);
	}
	var arreter=false;
	$("#"+nomDuCadre).click(function(){arreter=true;document.getElementById("loaderProvisoire").parentNode.removeChild(document.getElementById("loaderProvisoire"));montrerResultats("cadreProches");carrousel("cadreCoverflow");})
	var compteur=0;
	function inOut(compteur){$("#cache"+(compteur%14)).fadeOut(50,function(){if(arreter==false){inOut(compteur+1)}});$("#cache"+((compteur+9)%14)).fadeIn(50);}
	inOut(0);
	}
}
//{% load static %}

function loadChargement(nomDuCadre){
  
	var loader=document.createElement("div");
	loader.id="loaderProvisoire";
	loader.style.cssText='position:relative;width:300px;height:100%;margin:0 auto;z-index:10;'
	document.getElementById(nomDuCadre).appendChild(loader);
	var image=document.createElement("img");
	image.id="bandeauLoader";
	image.src="../pesto/static/img/explore/bandecine4.jpg";
	image.onload=function(){
	image.style.cssText='position:absolute;top:40%;left:0%;width:100%;height:20%;z-index:11;opacity:1;'
	document.getElementById("loaderProvisoire").appendChild(image);
	var cache=new Array;
	var position=new Array;
	position[0]=0.6;position[1]=7.6;position[2]=14.8;position[3]=22;position[4]=29;position[5]=36.1;
	position[6]=43.05;position[7]=50.5;position[8]=57.6;position[9]=64.7;position[10]=71.9;position[11]=78.9;
	position[12]=86.1;position[13]=92.9;
	var largeur=new Array;
	largeur[0]=5.8;largeur[1]=6.1;largeur[2]=5.9;largeur[3]=5.9;largeur[4]=6;largeur[5]=6;
	largeur[6]=6;largeur[7]=6;largeur[8]=6.1;largeur[9]=6;largeur[10]=6;largeur[11]=6.1;
	largeur[12]=5.8;largeur[13]=6.1;
	for(var i =0; i<14;i++){	
		cache[i]=document.createElement("div");
		cache[i].id="cache"+i;
		cache[i].style.cssText='position:absolute;top:43.4%;left:'+position[i]+'%;width:'+largeur[i]+'%;height:13.3%;z-index:12;background-color:#b0c4de;opacity:1;'//'+(i+1+i*6)+'
		document.getElementById("loaderProvisoire").appendChild(cache[i]);
	}
	document.getElementById(nomDuCadre).style.zIndex=10;
	document.getElementById(nomDuCadre).style.display="";
	/*var cachetest=document.createElement("div");
	cachetest.style.cssText="position:relative;top:43.5%;left:42%;width:100%;height:20%;"
	document.getElementById("loaderProvisoire").appendChild(cachetest);*/
	var arreter=false;
	//$("#"+nomDuCadre).click(function(){arreter=true;document.getElementById("loaderProvisoire").parentNode.removeChild(document.getElementById("loaderProvisoire"));montrerResultats("cadreProches");carrousel("cadreCoverflow");})
	var compteur=0;
	function inOut(compteur){$("#cache"+(compteur%14)).fadeOut(50,function(){if(arreter==false){inOut(compteur+1)}});$("#cache"+((compteur+9)%14)).fadeIn(50);}
	inOut(0);
	}
}

function unloadChargement(nomDuCadre){
	document.getElementById(nomDuCadre).style.zIndex=-1;
	document.getElementById(nomDuCadre).style.display="none";
	arreter=true;
	document.getElementById(nomDuCadre).removeChild(document.getElementById("loaderProvisoire"));
}

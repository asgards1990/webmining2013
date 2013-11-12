$(document).ready(function(){
	document.getElementById("results").style.position="relative";
	document.getElementById("cadreResultats").style.position="relative";
	//document.getElementById("cadreResultats").style.overflow="auto";
	/*var surSousCadreResultats =document.createElement("div");
	surSousCadreResultats.id="surSousCadreResultats";
	surSousCadreResultats.style.cssText="width:100%;height:100%; position: relative; margin-right:2%;"*/
	var sousCadreResultats =document.createElement("div");
	sousCadreResultats.id="sousCadreResultats";
	sousCadreResultats.style.cssText="width:100%;height:31.7em; position: absolute;top:0px;left:0px; margin-right:2%;z-index:-1;background-color:rgba(150,150,150,0.8);display:none;"
	var sousCadreResultats2 =document.createElement("div");
	sousCadreResultats2.id="sousCadreResultats2";
	sousCadreResultats2.style.cssText="width:100%;height:100%; position: relative;margin-right:2%;z-index:0;opacity:1;background-color:White;"
	var surCadreCoverflow = document.createElement("div");
	surCadreCoverflow.style.cssText="float:left;width:99%;height:7em;border-bottom: 1px solid grey; #000;margin:2em auto 2em auto;z-index:1"
	surCadreCoverflow.id="surCadreCoverflow";
	var cadreCoverflow = document.createElement("div");
	cadreCoverflow.style.cssText="position:relative;margin-left:auto;margin-right:auto;width:435px;height:103px;z-index:2"
	cadreCoverflow.id="cadreCoverflow";
	var cadreProches = document.createElement("div");
	cadreProches.style.cssText="position:relative;float:left;width:76%;height:20em;margin-right:2%; #000;z-index:2"
	cadreProches.id="cadreProches";
	var cadreInfo = document.createElement("div");
	cadreInfo.style.cssText="float:left;width:20%;height:20em;z-index:2"//border:1px solid #000;"
	cadreInfo.id="cadreInfo";
	//document.getElementById("cadreResultats").appendChild(surSousCadreResultats);
	document.getElementById("results").appendChild(sousCadreResultats);
	document.getElementById("cadreResultats").appendChild(sousCadreResultats2);
	document.getElementById("sousCadreResultats2").appendChild(surCadreCoverflow);
	document.getElementById("surCadreCoverflow").appendChild(cadreCoverflow);
	document.getElementById("sousCadreResultats2").appendChild(cadreProches);
	document.getElementById("sousCadreResultats2").appendChild(cadreInfo);
	//loadChargement("cadreProches");
	//carrousel("cadreCoverflow");

});

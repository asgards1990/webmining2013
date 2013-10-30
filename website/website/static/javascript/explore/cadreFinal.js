$(document).ready(function(){
	var surCadreCoverflow = document.createElement("div");
	surCadreCoverflow.style.cssText="float:left;width:99%;height:7em;border:1px solid #000;margin:2em auto 2em auto"
	surCadreCoverflow.id="surCadreCoverflow";
	var cadreCoverflow = document.createElement("div");
	cadreCoverflow.style.cssText="position:relative;margin-left:auto;margin-right:auto;width:435px;height:103px;"
	cadreCoverflow.id="cadreCoverflow";
	var cadreProches = document.createElement("div");
	cadreProches.style.cssText="position:relative;float:left;width:76%;height:20em;margin-right:2%;border:1px solid #000;"
	cadreProches.id="cadreProches";
	var cadreInfo = document.createElement("div");
	cadreInfo.style.cssText="float:left;width:20%;height:20em;"//border:1px solid #000;"
	cadreInfo.id="cadreInfo";
	document.getElementById("cadreResultats").appendChild(surCadreCoverflow);
	document.getElementById("surCadreCoverflow").appendChild(cadreCoverflow);
	document.getElementById("cadreResultats").appendChild(cadreProches);
	document.getElementById("cadreResultats").appendChild(cadreInfo);
	loadChargement("cadreProches");
	//carrousel("cadreCoverflow");

});

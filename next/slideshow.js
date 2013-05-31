// Production steps of ECMA-262, Edition 5, 15.4.4.18
// Reference: http://es5.github.com/#x15.4.4.18
if ( !Array.prototype.forEach ) {
    Array.prototype.forEach = function( callback, thisArg ) {

	var T, k;

	if ( this == null ) {
		throw new TypeError( " this is null or not defined" );
	}

	// 1. Let O be the result of calling ToObject passing the |this| value as the argument.
	var O = Object(this);

	// 2. Let lenValue be the result of calling the Get internal method of O with the argument "length".
	// 3. Let len be ToUint32(lenValue).
	var len = O.length >>> 0; // Hack to convert O.length to a UInt32

	// 4. If IsCallable(callback) is false, throw a TypeError exception.
	// See: http://es5.github.com/#x9.11
	if ( {}.toString.call(callback) != "[object Function]" ) {
		throw new TypeError( callback + " is not a function" );
	}

	// 5. If thisArg was supplied, let T be thisArg; else let T be undefined.
	if ( thisArg ) {
		T = thisArg;
	}

	// 6. Let k be 0
	k = 0;

	// 7. Repeat, while k < len
	while( k < len ) {

		var kValue;

		// a. Let Pk be ToString(k).
		//	 This is implicit for LHS operands of the in operator
		// b. Let kPresent be the result of calling the HasProperty internal method of O with argument Pk.
		//	 This step can be combined with c
		// c. If kPresent is true, then
		if ( k in O ) {

			// i. Let kValue be the result of calling the Get internal method of O with argument Pk.
			kValue = O[ k ];

			// ii. Call the Call internal method of callback with T as the this value and
			// argument list containing kValue, k, and O.
			callback.call( T, kValue, k, O );
		}
		// d. Increase k by 1.
		k++;
	}
	// 8. return undefined
    };
}

/* The rest of this code is from Darrick. */
function addEventHandler(node, eventName, lambda)
{
	var cookie = {node: node, event: eventName, func: lambda};
	if (node.addEventListener)
		node.addEventListener(eventName, lambda, false);
	else if (node.attachEvent)
		node.attachEvent("on" + eventName, lambda);
	return cookie;
}

function get_slides()
{
	/* shiny new html5 thing */
	if (document.getElementsByClassName) {
		return document.getElementsByClassName("slide");
	}

	var res = Array();
	/* use xpath */
	if (document.evaluate) {
		var node = null;
		var nodes = document.evaluate("//*[@class = 'slide']", document, null, 0, null);
		while ((node = nodes.iterateNext())) {
			res.push(node);
		}
		return res;
	}

	/* shitty slow way for ie */
	var nodes = document.getElementsByTagName("*");
	for (var l = 0; l < nodes.length; l++) {
		if (nodes[l].className == 'slide') {
			res.push(nodes[l]);
		}
	}
	return res;
}

function Slider(element, classname, displayStyle)
{
	children = element.children;

	this.element = element;
	this.current = -1;
	this.layers = new Array();
	this.displayStyle = displayStyle;

	for (l = 0; l < children.length; l++) {
		if (children[l].className == classname) {
			this.layers.push(children[l]);
		}
	}

	for (l = 0; l < this.layers.length; l++) {
		if (this.current < 0 && this.layers[l].style.display == this.displayStyle) {
			this.current = l;
		}
	}

	if (this.current < 0) {
		this.current = 0;
		this.layers[0].style.display = this.displayStyle;
	}
}

Slider.prototype.next = function()
{
	c = this.current + 1;
	if (c >= this.layers.length)
		c = 0;
	this.slideTo(c);
}

Slider.prototype.previous = function()
{
	c = this.current - 1;
	if (c < 0)
		c = this.layers.length - 1;
	this.slideTo(c);
}

Slider.prototype.slideTo = function(c)
{
	this.layers[c].style.display = this.displayStyle;
	this.layers[this.current].style.display = "none";
	this.current = c;
}

function resizer()
{
	var win_width;
	if (typeof(window.innerWidth) != "undefined")
		win_width = window.innerWidth;
	else if (typeof(document.documentElement.offsetWidth) != "undefined")
		win_width = document.documentElement.offsetWidth;
	else if (typeof(document.body.offsetWidth) != "undefined")
		win_width = document.body.offsetWidth;

	var height = Math.floor(win_width / 1.82);
	if (height > 500)
		height = 500;
	var slides = get_slides();
	Array.prototype.forEach.call(slides, function(s) {s.style.height = height + "px";});
	
}
function createSlides(element)
{
	var slides = [
{caption: "Youth Weekend 2013", img: "http://www.youthweekendwest.com/group_pic.jpg", url: "http://youthweekendwest.com/"},
{caption: "2008 Ball", img: "http://djwong.org/photography/oregon/rscds_ball_2008/dsc_0052.jpg", url: "http://djwong.org/photography/oregon/rscds_ball_2008/"},
{caption: "Rose Festival, 2007", img: "http://djwong.org/photography/oregon/portland/rose_fest_2007/img_0304.jpg", url: "http://djwong.org/photography/oregon/portland/rose_fest_2007/"},
{caption: "2007 Ball", img: "http://djwong.org/photography/oregon/rscds_ball_2007/mmc_3772.jpg", url: "http://djwong.org/photography/oregon/rscds_ball_2007/"},
{caption: "2006 Ball", img: "http://djwong.org/photography/oregon/portland/rscds_ball06/a3110316.jpg", url: "http://djwong.org/photography/oregon/portland/rscds_ball06/"},
{stop: 1}
	];

	for (var l = 0; l < slides.length - 1; l++) {
		captionElement = document.createTextNode(slides[l].caption);
		captionDiv = document.createElement("a");
		captionDiv.href = slides[l].url;
		captionDiv.appendChild(captionElement);
		
		slideDiv = document.createElement("div");
		slideDiv.className = "slide";
		imgurl = "url('" + slides[l].img + "')";
		slideDiv.style.backgroundImage = imgurl;
		slideDiv.appendChild(captionDiv);

		itemDiv = document.createElement("div");
		itemDiv.className = "ss_item";

		itemDiv.appendChild(slideDiv);
		element.appendChild(itemDiv);
		addEventHandler(slideDiv, "onclick", function() {alert(slides[l].url);});
	}
}

var slider = null;
function load() {
	createSlides(document.getElementById("ss_cont"));
	slider = new Slider(document.getElementById("ss_cont"), "ss_item", "block");
	resizer();
	addEventHandler(window, "resize", resizer);
	setInterval(function() {slider.next();}, 15000);
}

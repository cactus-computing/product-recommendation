"use strict";



function productScroll() {
  let slider = document.getElementById("cross-sell-slide-box");
  let next = document.getElementsByClassName("pro-next");
  let prev = document.getElementsByClassName("pro-prev");
  let slide = document.getElementById("cross-sell-slide");
  let item = document.getElementById("cross-sell-slide");
  for (let i = 0; i < next.length; i++) {
    //refer elements by class name

    let position = 0; //slider postion
    let width = 210; // product box + margin width
    let visibleProductsWanted = 3;
    prev[i].addEventListener("click", function() {
      //click previos button
      if (position > 0) {
        //avoid slide left beyond the first item
        position -= 1;
        slide.scroll({ left: slide.scrollLeft -= visibleProductsWanted * width });
        console.log("izquierda");
        //translateX(position); //translate items
      }
    });

    next[i].addEventListener("click", function() {
      if (position >= 0 && position < hiddenItems()) {
        //avoid slide right beyond the last item
        position += 1;
        slide.scroll({ left: slide.scrollLeft += visibleProductsWanted * width });
        console.log("izquierda");
        //translateX(position); //translate items
      }
    });
  }

  function hiddenItems() {
    //get hidden items
    let items = getCount(item, false);
    let visibleItems = slider.offsetWidth / 210;
    return items - Math.ceil(visibleItems);
  }
}

function translateX(position) {
  //translate items
  let slide = document.getElementById("cross-sell-slide");
  let width = 210; //product box + margin width
  slide.scroll({ left: slide.scrollLeft += 630 });
  // slide.style.left = position * -210 + "px";
}

function getCount(parent, getChildrensChildren) {
  //count no of items
  let relevantChildren = 0;
  let children = parent.childNodes.length;
  for (let i = 0; i < children; i++) {
    if (parent.childNodes[i].nodeType != 3) {
      if (getChildrensChildren)
        relevantChildren += getCount(parent.childNodes[i], true);
      relevantChildren++;
    }
  }
  return relevantChildren;
}
const button=
document.getElementById(
"generate"
)

const textarea=
document.getElementById(
"prompt"
)

const palette=
document.getElementById(
"palette"
)

const history=
document.getElementById(
"history"
)

const toast=
document.getElementById(
"toast"
)

const copyAll=
document.getElementById(
"copyAll"
)

const download=
document.getElementById(
"download"
)

const share=
document.getElementById(
"share"
)

const scheme=
document.getElementById(
"scheme"
)


button.onclick=
generate

copyAll.onclick=
copyAllHex

download.onclick=
downloadPNG

share.onclick=
shareLink


textarea.addEventListener(

"keydown",

event=>{

if(

event.key==="Enter"

&&

!event.shiftKey

){

event.preventDefault()

generate()

}

}

)


loadHistory()

restoreFromUrl()



async function generate(){

const text=

textarea.value.trim()

if(
!text
)
return


const response=

await fetch(

"/api/generate",

{

method:"POST",

headers:{

"Content-Type":
"application/json"

},

body:

JSON.stringify({

text:text,

scheme:
scheme.value,

creativity:0.5

})

}

)


const data=

await response.json()


renderPalette(
data.palette
)


saveHistory(

text,

data.palette

)

}



function renderPalette(
colors
){

palette.innerHTML=""

window.currentColors=
colors


colors.forEach(

(color,index)=>{


const div=

document.createElement(
"div"
)


div.className=
"color"


div.style.animationDelay=

`${index*0.1}s`


div.innerHTML=`

<div

class="box"

title="${color.name}"

style="
background:${color.hex}
"

></div>

<div
class="hex"
>
${color.hex}
</div>

`


div.querySelector(

".box"

).onclick=()=>{

navigator
.clipboard
.writeText(
color.hex
)

showToast(
"Copied"
)

}


palette.appendChild(
div
)

}

)

}



function saveHistory(
query,
paletteData
){

let items=

JSON.parse(

localStorage.getItem(

"moodpalette.history"

)

||

"[]"

)


items=

items.filter(
x=>x.query!==query
)


items.unshift({

query:query,

palette:paletteData

})


items=
items.slice(
0,
20
)


localStorage.setItem(

"moodpalette.history",

JSON.stringify(
items)

)


loadHistory()

}



function loadHistory(){

history.innerHTML=""


const items=

JSON.parse(

localStorage.getItem(
"moodpalette.history"
)

||

"[]"

)


items.forEach(

item=>{

const div=

document.createElement(
"div"
)

div.className=
"historyItem"

div.innerText=
item.query


div.onclick=()=>{

textarea.value=
item.query

renderPalette(
item.palette
)

}


history.appendChild(
div
)

}

)

}



function copyAllHex(){

if(
!window.currentColors
)
return


const text=

window.currentColors

.map(
x=>x.hex
)

.join(",")


navigator
.clipboard
.writeText(
text
)


showToast(
"All HEX copied"
)

}



function downloadPNG(){

if(
!window.currentColors
)
return


const colors=

window.currentColors

.map(
x=>x.hex
)

.join(",")


window.open(

"/api/export?colors="+

encodeURIComponent(
colors
)

)

}



function shareLink(){

const text=

textarea.value.trim()

if(
!text
)
return


const params=

new URLSearchParams({

q:text,

s:scheme.value,

c:"0.5"

})


const url=

window.location.origin+

"/?"+

params.toString()


navigator
.clipboard
.writeText(
url
)

showToast(
"Link copied"
)

}



function restoreFromUrl(){

const params=

new URLSearchParams(

window.location.search

)

const query=

params.get(
"q"
)

const urlScheme=

params.get(
"s"
)


if(
!query
)
return


textarea.value=
query


if(
urlScheme
){

scheme.value=
urlScheme

}


generate()

}



function showToast(
message
){

toast.innerText=
message

toast.classList.add(
"show"
)

setTimeout(

()=>{

toast.classList.remove(
"show"
)

},
1000

)

}
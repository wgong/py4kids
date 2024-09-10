/*

> npm i cnchar
> npm i 
cnchar-code
cnchar-draw
cnchar-explain
cnchar-idiom
cnchar-info
cnchar-input
cnchar-name
cnchar-order
cnchar-poly
cnchar-radical
cnchar-random
cnchar-trad
cnchar-voice
cnchar-words
cnchar-xhy

> node demo-1.js

*/

// 请保证最先引入 cnchar 基础库，其他几个库顺序无所谓
var cnchar = require('cnchar');
var poly = require('cnchar-poly');
cnchar.use(poly); 

var idiom = require('cnchar-idiom');
cnchar.use(idiom); 

var explain = require('cnchar-explain');   // not working
cnchar.use(explain); 

var trad = require('cnchar-trad');   // not working
cnchar.use(trad); 

var radical = require('cnchar-radical');   // not working
cnchar.use(radical); 

var words = require('cnchar-words');   // not working
cnchar.use(words); 

var info = require('cnchar-info');   // not working
cnchar.use(info); 

var xhy = require('cnchar-xhy');   // not working
cnchar.use(xhy); 

// ... 其他插件请参考第二章 2. 功能及插件概览
// 插件请按需取用
// 注：cnchar-draw，cnchar-voice 在非浏览器环境下不可使用

// spell, stroke
zi = '好';
// console.log(zi.spell()); // prototype 方式调用
console.log(cnchar.spell(zi)); // cnchar api 调用
console.log(cnchar.stroke(zi)); // cnchar api 调用


// explain
// console.log(cnchar.explain('你好')); // cnchar api 调用
// Not working: got Promise { <pending> }

zi = "龚汉";
zi_2 = cnchar.convert.simpleToTrad(zi);
console.log(zi_2); // 简体 => 繁体
zi_2_a = cnchar.convert.tradToSimple(zi_2); // 繁体 => 简体
console.log(zi_2_a); // 繁体 => 简体

zi = "牜";
zi_2 = cnchar.radical.radicalToWord(zi);
console.log(zi_2); // 简体 => 繁体


zi = "日火汉字";
zi_2 = cnchar.info(zi);
console.log(zi_2); // 

for (const c of ['a','1','？','国','國']) {
    console.log(c)
    console.log(cnchar.isCnChar(c))
}

// 歇后语
// cnchar.xhy('大水冲了龙王庙') 
// ['大水冲了龙王庙-自家人不识自家人', '大水冲了龙王庙-一家人不认一家人']
zi = "大水冲了龙王庙";
zi_2 = cnchar.xhy(zi);
console.log(zi_2); 

// cnchar.xhy('大水', 'fuzzy') 
// ['江河里长大水-泥沙俱下', '江河发大水-后浪推前浪', ... ]
zi = "大水";
zi_2 = cnchar.xhy(zi, 'fuzzy');
console.log(zi_2); 

// cnchar.xhy('大水', 'fuzzy', 'answer') 
// ['泥沙俱下', '后浪推前浪', ... ]
zi = "大水";
zi_2 = cnchar.xhy(zi, 'fuzzy', 'answer');
console.log(zi_2); 

// cnchar.xhy('上晃下摇', 'fuzzy', 'answer', 'second') 
// ['醉汉过铁索桥', '扶着醉汉过破桥']
zi = "上晃下摇";
zi_2 = cnchar.xhy(zi, 'fuzzy', 'answer', 'second');
console.log(zi_2); 

// idiom
zi = "日";
console.log("Words"); // 

zi_2 = cnchar.words(zi);
console.log(zi_2); // 

console.log("Idioms"); // 
console.log(cnchar.idiom([zi, '', '', '']));  
console.log(cnchar.idiom(['', zi, '', '']));  
console.log(cnchar.idiom(['', '', zi, '']));  
console.log(cnchar.idiom(['', '', '', zi]));  


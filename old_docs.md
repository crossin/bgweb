# Introduction #
old documents record some problems solved before
Add your content here.
bug to be fixed
. the & encode problem
在原来的版本能够正常工作，但是移植后出现了问题，
问题是&被两次编码了，具体位置没有发现
&amp; 成了&amp;amp这就造成问题了，最要命的是有些URL链接未收到影响而有的链接受到了影响


problem is found
1.DJANGO 1.0以后的版本 TEMPLATE里支持了AUTO ESCAPE，即对字符串里的任何
转移字符，DJANGO都会进行转义，这就造成了问题
因为从RSS里获得的内容本身就是带有转义后的字符的
API的前向不兼容造成的

http://www.chickenwingsw.com/scratches/python/escaping-autoescape-in-django

TAGGING的需求不明确，目前的打算先做成供ADMIN分类的子功能

view links in different sort

对于parse相关的内容不能设置为NONE

2010-4-23 TITLELINK CHANGED TO MULTI-LINE

# Details #

**heritage document**
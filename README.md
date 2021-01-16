# SQSS(simple qss)
在qt的中的qss预编译语言，加强qss的可维护性

## 语法构成

### 对象关系
```js
const Obj = {
  var: {
    num: {
      val:    Number
      , unit: String
    }
    , str: String
    , fun: Function

    , map: Map
    , arr: Array
  }
  , selector: {
  }
}
```

### 语法解析

`selector | property: var | $var-name: var | @macro args`
```
@defineProperty w width
@defineProperty h height

$size: 100px
.main::slot-a[is-show=true]
  w: $size
  h: $size
  font: 10px
    weight: bold

  > .top, > .content
    $size:
	  w: $size
    w: $size.w

  > .top
    h: 40px
    background-color: rgba(255, 255, 255, .8)
    .icon
      &:hover
        color: rgb(255, 255, 255)
      &:!hover
        color: rgb(0, 0, 0)
	  &[:hover, :!hover]
	    w: 40px
		h: 40px
    .title
      color: black
      &[type='primary']
        color: blue
      &[type='danger']
        color: red
```
```js
const rootScope = {
  scopes: [{
	selectors: [{
	  name: '.main'
      , root:    root()
      , parrent: preNode()
	  , subControl: {
		'slot-a': {
		  'is-show': true
		}
	  }
	}]
    , vars: {
	  'size': {
		'w': vars('size'),
	  }
	}
	, properties: {
	  'w': vars('size'),
	  'h': vars('size'),
	  'font': {
		val: num(10, 'px'),
		properties: {
		  'weight': str('bold')
		}
	  }
	}
  }]
  , vars: {
    'size': num(100, 'px')
  }
  , macros: {
    'size': macro('defineProperty', [ w, width ])
  }
}
```

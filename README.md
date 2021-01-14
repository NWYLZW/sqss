# SQSS(simple qss)
在qt的中的qss预编译语言，加强qss的可维护性

## 语法构成

### 对象关系
```js
const Obj = {
  var: {
    num: {
      val:    Interger | Number
      , unit: String
    }
    , str: String
    , fun: Function

    , map: Map
    , array: Array
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
.main(:hover, :clicked)::slot-a[is-show=true]
  w: $size
  h: $size
  font: 10px
    weight: bold

  $size:
    w: $size
    h: 40px
  > .top
    w: $size.w
    h: $size.h
    background-color: rgba(255, 255, 255, .8)
    .icon
      &:hover
        color: rgb(255, 255, 255)
      &:!hover
        color: rgb(0, 0, 0)
    .title
      color: black
      &[type='primary']
        color: blue
      &[type='danger']
        color: red
```
```js
const module = {
  selectors: {
    '.main': {
      pseudoClass: {
        or: [ 'hover', 'clicked' ]
      }
      , subControl: {
        'slot-a': {
          'is-show': true
        }
      }
      , properties: {
        'w': vars('$size'),
        'h': vars('$size'),
        'font': {
          val: num(10, 'px'),
          properties: {
            'weight': str('bold')
          }
        }
      }
    }
  }
  , vars: {
    'size': num(100, 'px')
  }
  , macros: {
    'size': macro('defineProperty', [ w, width ])
  }
}
```

const gulp = require('gulp')
const {src,dest,series} = gulp
const uglifycss = require('gulp-uglifycss')
const uglify = require('gulp-uglify')
const babel = require('gulp-babel')
const htmlmin = require('gulp-htmlmin')

function css(){
    return src('coisas/dev/css/*.css')
        .pipe(uglifycss({
            "uglyComments":true
        })).pipe(dest('static/assets/css'))
}

function js(){
    return src('coisas/dev/js/*.js')
    .pipe(babel({
        "presets":["env"]
    })).pipe(uglify())
    .pipe(dest('static/assets/js'))
}

function html(){
    return src('coisas/dev/paginas/*.html')
        .pipe(htmlmin({
            collapseWhitespace:true
        })).pipe(dest('cliente/templates'))
}

module.exports.default = series(
    html,
    css,
    js
)
/* eslint-disable import/no-extraneous-dependencies */
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
require('@babel/polyfill');
const path = require('path');

module.exports = {
    context: __dirname,
    entry: {
        main: './src/main',
    },
    output: {
        path: path.resolve('./static/demo'),
        publicPath: path.resolve('./static/demo'),
    },
    plugins: [
        new BundleTracker({ filename: './webpack-stats.json' }),
        new VueLoaderPlugin(),
    ],
    module: {
        rules: [
            {
                test: /\.m?js$/,
                include: path.resolve('./assets/js'),
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env'],
                    },
                },
            },
            {
                test: /.(jpg|png|woff(2)?|eot|ttf)$/,
                loader: 'file-loader',
            },
            {
                test: /\.svg$/,
                oneOf: [
                    {
                        loader: 'file-loader',
                    },
                ],
            },
            {
                test: /\.vue$/,
                use: [
                    { loader: 'vue-loader' },
                ],
            },
        ],
    },
    resolve: {
        modules: ['./node_modules'],
        extensions: ['*', '.js'],
        alias: {
            vue$: 'vue/dist/vue.esm.js',
            assets: path.resolve('./assets'),
        },
    },
};

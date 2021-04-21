/* eslint-disable import/no-extraneous-dependencies */
const { merge } = require('webpack-merge');
const autoprefixer = require('autoprefixer');
const tailwindcss = require('tailwindcss');
const path = require('path');
const glob = require('glob');
const CleanWebpackPlugin = require('clean-webpack-plugin');
const TerserWebpackPlugin = require('terser-webpack-plugin');
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const common = require('./webpack.common');

module.exports = merge(common, {
    mode: 'production',
    output: {
        filename: '[name]-[hash].js',
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: '[name]-[hash].css',
            chunkFilename: '[id]-[hash].css',
        }),
        new CleanWebpackPlugin(['./static/demo']),
        new OptimizeCSSAssetsPlugin({}),
    ],
    devtool: 'source-map',
    optimization: {
        minimizer: [new TerserWebpackPlugin()],
    },
    module: {
        rules: [
            {
                test: /\.(sa|sc|c)ss$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    {
                        loader: 'css-loader',
                        options: { sourceMap: true },
                    },
                    {
                        loader: 'postcss-loader',
                        options: {
                            sourceMap: true,
                            plugins: () => [tailwindcss, autoprefixer],
                        },
                    },
                    {
                        loader: 'sass-loader',
                        options: {
                            sourceMap: true,
                            includePaths: glob.sync('node_modules').map((d) => path.join(__dirname, d)),
                        },
                    },
                ],
            },
        ],
    },
});

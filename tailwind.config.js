module.exports = {
    purge: {
        enabled: process.env.ENV === 'production',
        content: [
            './landing/demos/**/*.html',
            './landing/demos/**/*.vue',
            './landing/demos/**/*.jsx',
        ],
    },
    darkMode: false, // or 'media' or 'class'
    theme: {
        extend: {
            colors: {
                'cactus-blue': '#278ddd',
                'cactus-green': '#1de38f',
            },
        },
    },
    variants: {
        extend: {},
    },
    plugins: [
        require('@tailwindcss/line-clamp'),
    ],
};

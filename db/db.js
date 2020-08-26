const { Pool } = require('pg');

const pool = new Pool({
    user: 'postgres',
    host: 'phantomdb.cstig7wsxqtk.us-west-2.rds.amazonaws.com',
    database: 'knorrstats',
    password: 'gayisabsolutelynotokay',
    port: 5432,
});

/* IGNORE CODE BELOW ITS AN EXAMPLE
const getArticle = async (url) => (await pool.query("SELECT title, created_on, body, thumbnail_url, thumbnail_caption FROM article WHERE is_published AND seo_url = $1 LIMIT 1;",
    [url])).rows.map(row => {
        return {
            title: row.title,
            date: row.created_on,
            thumbnailUrl: row.thumbnail_url,
            body: row.body,
            caption: row.thumbnail_caption
        };
    });*/

module.exports = {
    query: (text, params) => pool.query(text, params),
};

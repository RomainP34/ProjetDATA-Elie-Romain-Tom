const mongoose = require('mongoose');

const categorySchema = mongoose.Schema(
    {
        name: {
            type: String,
            required: true
        },
        id: {
            type: Number,
            required: true
        }
    }
)

module.exports = mongoose.model('Categories', categorySchema);
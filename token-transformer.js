    const fs = require('fs');
    const { transform } = require('token-transformer');

    // GitHub-аас авсан tokens.json файлын эх хувилбар
    const figmaTokens = JSON.parse(fs.readFileSync('./tokens.json', 'utf8'));

    // Зөвхөн Global болон Theme сетүүдийг ашиглах
    const setsToInclude = ['global', 'theme']; 
    const resolved = transform({
        tokens: figmaTokens,
        setsToInclude,
        // Semantic, Alias токенуудыг бодит утгаар нь солих
        resolveReferences: true 
    });

    // Хувиргасан үр дүнг хадгалах
    fs.writeFileSync('./transformed-tokens.json', JSON.stringify(resolved, null, 2));

    console.log('Figma tokens transformed successfully!');
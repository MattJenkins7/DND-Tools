function formatFeaturesText(input) {
    // Replace literal "\n" with actual line breaks
    return input.replace(/\\n/g, '\n');
}

// Example usage
const rawText = "Feat: Musician - Inspire allies during rests, proficiency with instruments.\\n\\nAlso noted in Proficiencies/Languages:\\nFeat: Musician - Inspire allies during rests, proficiency with instruments.";
const formattedText = formatFeaturesText(rawText);
console.log(formattedText); // Outputs text with proper line breaks

/**
 * Format a date string according to the specified format
 * @param {string} dateString - The date string to format
 * @param {string} format - The desired format ('HH:mm', 'MMM DD, YYYY', etc.)
 * @returns {string} - Formatted date string
 */
export const formatDateTime = (dateString, format) => {
  if (!dateString) return '';
  
  const date = new Date(dateString);
  
  // Return empty string for invalid dates
  if (isNaN(date.getTime())) return '';
  
  // Format according to the requested format
  switch (format) {
    case 'HH:mm':
      return `${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
      
    case 'MMM DD, YYYY':
      const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
      const month = months[date.getMonth()];
      const day = date.getDate();
      const year = date.getFullYear();
      return `${month} ${day}, ${year}`;
      
    default:
      return date.toLocaleString();
  }
}; 
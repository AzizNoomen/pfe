export interface FileItem {
    file: File;
    isAllowed: boolean;
    isDuplicate?: boolean;
    state?: 'in' | 'out'; // Optional property for animation state
    isRemoving?: boolean; // Optional property to indicate removal
}

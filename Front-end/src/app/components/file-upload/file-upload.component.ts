import { HttpEvent, HttpEventType } from '@angular/common/http';
import { AfterViewChecked, AfterViewInit, ChangeDetectorRef, Component, ElementRef, HostListener, ViewChild } from '@angular/core';
import { filesAnimations } from '../../animations/file-upload.animations';
import { ALLOWED_EXTENSIONS, DRAG_BOX_INSTRUCTION_ACTIVE, DRAG_BOX_INSTRUCTION_DEFAULT, FILE_REMOVE_ANIMATION_DURATION, FILE_REMOVE_DELAY } from '../../constants/file-upload.constants';
import { DropdownOption1, DropdownOption2 } from '../../enums/ingestion_dropdowns.enum';
import { FileStatus } from '../../enums/file-upload.enum';
import { FileItem } from '../../interfaces/file-upload.interface';
import { FileUploadService } from '../../services/file-upload/file-upload.service';


@Component({
  selector: 'app-file-upload',
  templateUrl: './file-upload.component.html',
  styleUrls: ['./file-upload.component.css'],
  animations: [
    filesAnimations
  ]
})


export class FileUploadComponent implements AfterViewInit, AfterViewChecked {
  @ViewChild('fileList') fileList!: ElementRef<HTMLUListElement>;
  @ViewChild('fileUploadBox') fileUploadBox!: ElementRef<HTMLDivElement>;
  @ViewChild('fileInstruction') fileInstruction!: ElementRef<HTMLSpanElement>;
  @ViewChild('fileBrowseInput') fileBrowseInput!: ElementRef<HTMLInputElement>;

  fileListItems: FileItem[] = [];
  uploadProgress: number[] = [];
  uploadStatus: string[] = [];
  completedFiles = 0;
  showDragBox = true;
  draggingFiles = false;
  isScrollingToBottom = true;
  filesSubmitted = false;
  allowedFiles = false;
  unallowedFiles: { file: File; displayTime: number }[] = [];
  duplicates: { file: File; displayTime: number }[] = [];
  isUploading = false;
  
  dropdownOpen1 = false;
  dropdownOpen2 = false;
  selectedOption1: string | null = 'Zephyr 7B';
  selectedOption2: string | null = 'Regular';
  dropdownOptions1 = Object.values(DropdownOption1);
  dropdownOptions2 = Object.values(DropdownOption2);
  showSettings = false;
  iconRotated = false;
  settingsVisible = false;

  
  constructor(
    private fileUploadService: FileUploadService,
    private cdr: ChangeDetectorRef
  ) {}

  ngAfterViewInit() {
    this.updateDragBoxInstructions(DRAG_BOX_INSTRUCTION_DEFAULT);

  }


  ngAfterViewChecked() {
    if (this.isScrollingToBottom) {
      this.scrollToBottom();
    }
  }

  @HostListener('dragenter', ['$event'])
  onDragEnter(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    if (this.isDragEventInsideBox(event)) {
      this.draggingFiles = true;
      this.updateDragBoxInstructions(DRAG_BOX_INSTRUCTION_ACTIVE);
      this.setDragBoxActive(true);
    }
  }

  @HostListener('dragover', ['$event'])
  onDragOver(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    if (this.isDragEventInsideBox(event)) {
      this.fileUploadBox.nativeElement.classList.add('active');
      this.setDragBoxActive(true);
    }
  }

  @HostListener('dragleave', ['$event'])
  onDragLeave(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    if (!this.isDragEventInsideBox(event)) {
      this.draggingFiles = false;
      this.setDragBoxActive(false);
      this.fileUploadBox.nativeElement.classList.remove('active');
      this.updateDragBoxInstructions(DRAG_BOX_INSTRUCTION_DEFAULT);
    }
  }

  @HostListener('drop', ['$event'])
  onDrop(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    this.draggingFiles = false;
    this.setDragBoxActive(false);
    if (this.isDragEventInsideBox(event) && event.dataTransfer) {
      this.handleSelectedFiles(event.dataTransfer.files);
    }
    this.fileUploadBox.nativeElement.classList.remove('active');
    this.updateDragBoxInstructions(DRAG_BOX_INSTRUCTION_DEFAULT);
  }

  @HostListener('change', ['$event'])
  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files) {
      this.handleSelectedFiles(input.files);
    }
  }

  onFileBrowseButtonClick(): void {
    if (this.fileBrowseInput) {
      this.fileBrowseInput.nativeElement.click();
    }
  }

  handleSelectedFiles(files: FileList): void {
    if (files.length === 0) return;

    const existingFiles = new Set(this.fileListItems.map(f => f.file.name.toUpperCase()));

    const newFiles = Array.from(files).map(file => {
      const fileExtension = this.getFileExtension(file.name);
      const isAllowed = ALLOWED_EXTENSIONS.includes(`.${fileExtension}`);
      const isDuplicate = existingFiles.has(file.name.toUpperCase());

      if (!isAllowed) {
        this.unallowedFiles.push({ file, displayTime: Date.now() });
      } else if (isDuplicate) {
        this.duplicates.push({ file, displayTime: Date.now() });
      }

      return { file, isAllowed, isDuplicate };
    });

    // Add new files
    newFiles.forEach(({ file, isAllowed, isDuplicate }) => {
      if (!existingFiles.has(file.name.toUpperCase()) || this.duplicates.find(item => item.file.name === file.name)) {
        this.fileListItems.push({ file, isAllowed, isDuplicate, state: 'in' }); // Add state property
        this.uploadProgress.push(0); // Initialize progress
        this.uploadStatus.push(isDuplicate ? FileStatus.DUPLICATE_FILE : !isAllowed ? FileStatus.UNSUPPORTED_EXTENSION : FileStatus.READY_TO_UPLOAD);
      }
    });

    // Remove extra copies of duplicates and unallowed files after a delay
    this.removeExtraCopiesAfterDelay();
  }

  removeExtraCopiesAfterDelay(): void {
    this.allowedFiles = false;
    setTimeout(() => {
      // Filter to keep one instance of each duplicate file
      const seenFiles = new Set<string>();
      const filteredFiles = this.fileListItems.filter(item => {
        if (seenFiles.has(item.file.name.toUpperCase())) {
          return false; // Exclude duplicates
        } else {
          seenFiles.add(item.file.name.toUpperCase());
          return true; // Include the first instance
        }
      });

      // Remove unallowed files
      const allowedFiles = filteredFiles.filter(item => item.isAllowed);
      // Update file list
      this.fileListItems = allowedFiles;

      // Update progress and status arrays
      this.uploadProgress = this.fileListItems.map(() => 0);
      this.uploadStatus = this.fileListItems.map(item =>
        item.isAllowed ? FileStatus.READY_TO_UPLOAD : FileStatus.UNSUPPORTED_EXTENSION
      );

      // Clear unallowed files and duplicates
      this.unallowedFiles = [];
      this.duplicates = [];
      this.allowedFiles = true;
    }, FILE_REMOVE_DELAY); // Display for defined delay
  }

  updateDragBoxInstructions(instruction: string): void {
    if (this.fileInstruction) {
      this.fileInstruction.nativeElement.innerText = instruction;
    }
  }

  getFileExtension(fileName: string): string {
    return fileName.split('.').pop()?.toUpperCase() || '';
  }

  getFileSize(sizeInBytes: number): string {
    return (sizeInBytes / (1024 * 1024)).toFixed(2) + ' MB';
  }

  submitFiles(): void {
    if (this.fileListItems.length === 0) return;
  
    this.filesSubmitted = true;
    this.isUploading = true; // Show spinner when upload starts
    this.showDragBox = false;
  
    this.uploadStatus = this.fileListItems.map(() => FileStatus.UPLOADING);
    this.isScrollingToBottom = false;

    // Set default values for chunking method and model name
    const modelName = this.selectedOption1?.split(' ')[0].toLowerCase() + ':latest' || 'zephyr:latest';
    const chunkingMethod = this.selectedOption2?.toLowerCase() || 'regular';
    
    console.log('selected option 1', this.selectedOption1?.split(' ')[0].toLowerCase() + ':latest' );
    console.log('selected option 2', this.selectedOption2?.toLowerCase());

    this.fileUploadService.uploadFiles(this.fileListItems.map(item => item.file), chunkingMethod, modelName).subscribe(
      (event: HttpEvent<any>) => {
        if (event.type === HttpEventType.UploadProgress) {
          const progress = Math.round((100 * event.loaded) / (event.total || 1));
          this.uploadProgress = this.fileListItems.map(() => progress);
        } else if (event.type === HttpEventType.Response) {
          this.uploadProgress = this.fileListItems.map(() => 100);
          this.uploadStatus = this.fileListItems.map(() => FileStatus.UPLOAD_COMPLETE);
          this.completedFiles = this.fileListItems.length;
          this.filesSubmitted = false;
          this.isUploading = false; // Hide spinner when upload is complete
        }
      },
      (error) => {
        this.uploadStatus = this.fileListItems.map(() => FileStatus.UPLOAD_FAILED);
        this.filesSubmitted = false;
        this.isUploading = false; // Hide spinner even if upload fails
        this.showDragBox = true;
        console.error('Upload error:', error);
      }
    );
  }
  

  cancelUpload(index: number): void {
    this.fileListItems[index].state = 'out'; // Set the state to 'out' for animation
    this.fileListItems[index].isRemoving = true; // Mark the file as removing

    setTimeout(() => {
      // Remove the item from the list after animation
      this.fileListItems.splice(index, 1);
      this.uploadProgress.splice(index, 1);
      this.uploadStatus.splice(index, 1);

      // Update the file list items' status
      this.uploadStatus = this.fileListItems.map(item =>
        item.isAllowed ? FileStatus.READY_TO_UPLOAD : FileStatus.UNSUPPORTED_EXTENSION
      );
      this.uploadProgress = this.fileListItems.map(() => 0);

      // Reset the removing state
      this.fileListItems.forEach(item => item.isRemoving = false);
      this.cdr.detectChanges();
    }, FILE_REMOVE_ANIMATION_DURATION); // Match this with the duration of your animation
  }

  getStatusClass(status: string): string {
    switch (status) {
      case FileStatus.UPLOAD_COMPLETE:
        return 'status-complete';
      case FileStatus.UPLOAD_FAILED:
        return 'status-failed';
      case FileStatus.UPLOADING:
        return 'status-progress';
      case FileStatus.DUPLICATE_FILE:
        return 'status-duplicate';
      case FileStatus.UNSUPPORTED_EXTENSION:
        return 'status-unallowed';
      case FileStatus.READY_TO_UPLOAD:
        return 'status-ready'; // Ensure this matches the class in CSS
      default:
        return ''; // Default case
    }
  }

  scrollToBottom(): void {
    if (this.fileList) {
      this.fileList.nativeElement.scrollTop = this.fileList.nativeElement.scrollHeight;
    }
  }

  isDragEventInsideBox(event: DragEvent): boolean {
    const dropArea = this.fileUploadBox.nativeElement.getBoundingClientRect();
    const x = event.clientX;
    const y = event.clientY;

    return x >= dropArea.left &&
            x <= dropArea.right &&
            y >= dropArea.top &&
            y <= dropArea.bottom;
  }

  setDragBoxActive(active: boolean): void {
    if (this.fileUploadBox) {
      if (active) {
        this.fileUploadBox.nativeElement.classList.add('active');
      } else {
        this.fileUploadBox.nativeElement.classList.remove('active');
      }
    }
  }


  toggleDropdown(dropdown: number) {
    if (dropdown === 1) {
      this.dropdownOpen1 = !this.dropdownOpen1;
    } else if (dropdown === 2) {
      this.dropdownOpen2 = !this.dropdownOpen2;
    }
  }

  selectOption(option: string, dropdown: number) {
    if (dropdown === 1) {
      this.selectedOption1 = option;
      this.dropdownOpen1 = false;
    } else if (dropdown === 2) {
      this.selectedOption2 = option;
      this.dropdownOpen2 = false;
    }
  }

  openSettings() {
    this.dropdownOpen1 = false;
    this.dropdownOpen2 = false;
    this.showSettings = true;
    setTimeout(() => this.settingsVisible = true, 300); // Show immediately
    this.iconRotated = !this.iconRotated;
  }

  closeSettings() {
    this.settingsVisible = false;
    setTimeout(() => this.showSettings = false, 300); // Delay to match animation
  }

}

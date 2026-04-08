const REPOSITORY_URL = "https://github.com/NickEsColR/job-candidate-matcher";

export function Footer() {
  return (
    <footer class="w-full border-t border-surface-container-low bg-background py-12">
      <div class="mx-auto flex max-w-screen-2xl items-center justify-center px-12 max-md:px-5">
        <p class="m-0 text-sm text-outline">
          <a
            href={REPOSITORY_URL}
            target="_blank"
            rel="noreferrer"
            class="text-outline underline-offset-4 transition-colors duration-200 hover:text-primary hover:underline"
          >
            © NickEsColR
          </a>
        </p>
      </div>
    </footer>
  );
}

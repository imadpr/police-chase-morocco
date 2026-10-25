POLICE CHASE MOROCCO - Android starter project

This is a Kivy/touch-control adaptation of the supplied Pygame game. It is not an APK yet.

Files:
- main.py: Android-friendly game implementation
- buildozer.spec: Android package settings
- .github/workflows/build-apk.yml: cloud build workflow
- police_siren.mp3: copy your siren file here (optional; without it, the game runs silently)

To build without installing Ubuntu on your Windows PC:
1. Create/sign in to a GitHub account.
2. Create a new repository, e.g. police-chase-morocco.
3. Upload the contents of this folder to the repository (including the hidden .github folder).
4. Open the repository's Actions tab and enable Actions if prompted.
5. Run the workflow named Build Android APK, or push a commit to main.
6. When the workflow finishes successfully, open the run and download the artifact named Police-Chase-Morocco-APK.
7. Extract the downloaded ZIP; install the APK on your Android phone. You may need to allow installing apps from your browser/file manager.

The first cloud build can take several minutes. The APK has not been built/tested in this environment.

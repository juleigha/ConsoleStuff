contents="contents.txt"
tempFile="temp.txt"
ftpFile="tmp.ftp"
> $tempFile
> $ftpFile
cat "boom.ftp" > $ftpFile
upload="false"
for localFolder in $( ls -d *Story/episode*);do
  read -r -u 3 chapterName
  read -r -u 3 folderName
  read -r -u 3 chapterImage
  read -r -u 3 publishDate
  read -r -u 3 folderSize
  echo "$chapterName  "
  if [ ! "$folderName" = "$localFolder" ]
  then
    read -p "Give $localFolder a name: " chapterName
    chapterImage="img"
    folderName=$localFolder
    publishDate=$(date)
    folderSize=$(du -s $localFolder)
    echo "mkdir $folderName" >> $ftpFile
    echo "cd $folderName" >> $ftpFile
    echo "! cd $localFolder" >> $ftpFile
    echo "mput *" >> $ftpFile
    echo "! cd .. " >> $ftpFile
    echo "cd .." >> $ftpFile
    upload="true"
  elif [ ! "$folderSize" = "$(du --summarize $localFolder)" ]
  then
    folderSize="$(du --summarize $localFolder)"
    echo "cd $folderName" >> $ftpFile
    echo "! cd $localFolder" >> $ftpFile
    echo "mput *" >> $ftpFile
    echo "! cd .. " >> $ftpFile
    echo "cd .." >> $ftpFile
    upload="true"
  fi
  echo "$chapterName" >> $tempFile
  echo "$folderName" >> $tempFile
  echo "$chapterImage" >> $tempFile
  echo "$publishDate" >> $tempFile
  echo "$folderSize" >> $tempFile
done 3< "$contents"
if [ "$upload" = "true" ]
then
  echo "bye" >> $ftpFile
  echo "uploading"
  # ftp -i -s:temp.ftp
fi
cat "$tempFile" > "$contents"

# rm $tempFile
# rm $ftpFile
read -p "Done. "

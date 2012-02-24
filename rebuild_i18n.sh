#! /bin/sh

I18NDOMAIN="s17.tinymce.mediaembed"

# Synchronise the templates and scripts with the .pot.
# All on one line normally:
i18ndude rebuild-pot --pot s17/tinymce/mediaembed/locales/${I18NDOMAIN}.pot \
    --create ${I18NDOMAIN} \
   s17/tinymce/mediaembed

# Synchronise the resulting .pot with all .po files
for po in s17/tinymce/mediaembed/locales/*/LC_MESSAGES/${I18NDOMAIN}.po; do
    i18ndude sync --pot s17/tinymce/mediaembed/locales/${I18NDOMAIN}.pot $po
done

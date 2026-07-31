import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagenArchivo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('contenido', models.BinaryField(editable=False)),
                ('content_type', models.CharField(max_length=100)),
                ('nombre_original', models.CharField(max_length=255)),
                ('tamano', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'imagenes_archivo',
            },
        ),
        migrations.AddField(
            model_name='servicio',
            name='imagen_archivo',
            field=models.ForeignKey(blank=True, db_column='imagen_archivo_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='catalogo.imagenarchivo'),
        ),
        migrations.AddField(
            model_name='evento',
            name='imagen_archivo',
            field=models.ForeignKey(blank=True, db_column='imagen_archivo_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='catalogo.imagenarchivo'),
        ),
        migrations.AddField(
            model_name='post',
            name='imagen_archivo',
            field=models.ForeignKey(blank=True, db_column='imagen_archivo_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='catalogo.imagenarchivo'),
        ),
        migrations.AddField(
            model_name='fotoevento',
            name='imagen_archivo',
            field=models.ForeignKey(blank=True, db_column='imagen_archivo_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='catalogo.imagenarchivo'),
        ),
        migrations.AlterField(
            model_name='fotoevento',
            name='imagen',
            field=models.TextField(blank=True, null=True),
        ),
    ]
